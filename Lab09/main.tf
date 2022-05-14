terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  credentials = "creds.json"
  project = "bgt-labs-20701"
  region  = "us-central1"
  zone    = "us-central1-a"
}

variable "setup_script_head" {
  type    = string
  default = "./SetupHead.sh"
}
variable "setup_script_worker" {
  type    = string
  default = "./SetupWorker.sh"
}

resource "google_compute_network" "ray-network" {
  name                    = "ray-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "ray-subnetwork" {
  depends_on    = [google_compute_network.ray-network]
  name          = "ray-subnetwork"
  ip_cidr_range = "192.168.0.0/24"
  region        = "us-central1"
  network       = google_compute_network.ray-network.id
  private_ip_google_access = true
}

resource "google_compute_firewall" "ssh-rule" {
  name = "ssh-rule"
  network = google_compute_network.ray-network.name
  allow {
    protocol = "tcp"
    #ports = ["22","6379"]
  }
  target_tags = ["https-server"]
  source_ranges = ["0.0.0.0/0"]
}
resource "google_compute_instance" "headnode" {
  name         = "headnode"
  machine_type = "e2-micro"
  depends_on   = [google_compute_subnetwork.ray-subnetwork]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 10
    }
  }
  network_interface {
    subnetwork = "ray-subnetwork"
    network_ip = "192.168.0.10"
    access_config {
      // Ephemeral public IP
    }
  }
  metadata_startup_script = file(var.setup_script_head)
  tags = ["http-server","https-server"]

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.ray-service-account.email
    scopes = ["cloud-platform"]
  }
}

resource "google_compute_instance" "workernode" {
  count        = 9
  depends_on   = [google_compute_instance.headnode]
  name         = "workernode-${count.index}"
  machine_type = "e2-micro"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 10
    }
  }
  network_interface {
    subnetwork = "ray-subnetwork"
    network_ip = "192.168.0.${count.index+2}0"
  }
  metadata_startup_script = file(var.setup_script_worker)
  tags = ["http-server","https-server"]

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.ray-service-account.email
    scopes = ["cloud-platform"]
  }
}

resource "google_service_account" "ray-service-account" {
  account_id   = "ray-service-account"
  display_name = "ray-service-account"
}

resource "google_project_iam_member" "datastore_owner_binding" {
  project = "bgt-labs-20701"
  role    = "roles/datastore.owner"
  member  = "serviceAccount:${google_service_account.ray-service-account.email}"
  depends_on = [google_service_account.ray-service-account]
}