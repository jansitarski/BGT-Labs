terraform {
    cloud {
    organization = "JanSitarski"

    workspaces {
      name = "BGTLab6"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  project     = "BGT-Labs-20701"
  credentials = "gcloudcredentials.json"
  region      = "us-central1"
  zone        = "us-central1-a"
}

resource "google_service_account" "defaultUser" {
  account_id   = "terraformcreated"
  display_name = "terraformCreated"
}

data "template_file" "default" {
  template = file("${path.module}/setupAndRun.sh")
}

resource "google_compute_instance" "FirstMachine" {
  name         = "firstMachine"
  machine_type = "n2-standard-2"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 50
    }
  }
  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = google_service_account.defaultUser.email
    scopes = ["cloud-platform"]
  }
  metadata_startup_script = file("./SetupAndRun.sh")

}
