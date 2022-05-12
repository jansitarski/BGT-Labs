terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  #credentials = "creds.json"
  project = "bgt-labs-20701"
  region  = "us-central1"
  zone    = "us-central1-a"
}

variable "setup_script" {
  type    = string
  default = "./Setup.sh"
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
    network_ip = "192.168.0.100"
    access_config {
      // Ephemeral public IP
    }
  }
  metadata_startup_script = file(var.setup_script)
}

resource "google_compute_instance" "workernode" {
  count        = 2
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
    network_ip = "192.168.0.${count.index}0"
    access_config {
      // Ephemeral public IP
    }
  }
  metadata_startup_script = file(var.setup_script)
}