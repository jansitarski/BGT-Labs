terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  project     = "BGT-Labs-20701"
  region      = "us-central1"
  zone        = "us-central1-a"
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
  metadata_startup_script = file("./SetupAndRun.sh")

}
