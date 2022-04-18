terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.15.0"
    }
  }
}

provider "google" {
  project     = "bgt-labs-20701"
  region      = "us-central1"
  zone        = "us-central1-a"
}

resource "google_compute_instance" "firstmachine" {
  name         = "firstmachine"
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

}/*
resource "google_compute_instance" "secondmachine" {
  name         = "secondmachine"
  machine_type = "n2-standard-4"

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
*/
resource "google_compute_instance" "thirdmachine" {
  name         = "thirdmachine"
  machine_type = "n2-standard-2"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100
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
/*
resource "google_compute_instance" "fourthmachine" {
  name         = "fourthmachine"
  machine_type = "n2-standard-4"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100
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
*/
