terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  project     = "bgt-labs"
  credentials = "gcloudcredentials.json"
  region      = "us-central1"
  zone        = "us-central1-a"
}

resource "google_service_account" "defaultUser" {
  account_id   = "terraformcreated"
  display_name = "terraformCreated"
}

data "template_file" "default" {
  template = file("${path.module}/setupScheduler.sh")
}

resource "google_compute_instance" "Scheduler" {
  name         = "dask-scheduler"
  machine_type = "e2-small"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network    = "default"
    network_ip = "10.128.0.2"
  }
  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.defaultUser.email
    scopes = ["cloud-platform"]
  }
  metadata_startup_script = file("./setupScheduler.sh")

}
/*
resource "google_compute_instance" "Worker" {
  name         = "dask-worker"
  machine_type = "e2-small"
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network    = "default"
    network_ip = "10.128.0.2"
  }
  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.defaultUser.email
    scopes = ["cloud-platform"]
  }
}


resource "google_compute_instance" "Client" {
  name         = "dask-client"
  machine_type = "e2-small"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }
  network_interface {
    network    = "default"
    network_ip = "10.128.0.3"
  }
  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.defaultUser.email
    scopes = ["cloud-platform"]
  }
}
*/