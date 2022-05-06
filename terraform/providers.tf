terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "2.9.7"
    }
  }
}

provider "proxmox" {
  # Configuration options
  pm_api_url = "https://172.16.203.129:8006/api2/json"
  # api token id is in the form of: <username>@pam!<tokenId>
  pm_api_token_id = "terraform_user@pam!tuser_token_id"
  # this is the full secret wrapped in quotes. don't worry, I've already deleted this from my proxmox cluster by the time you read this post
  pm_api_token_secret = "481e2c4a-a0b0-48c1-baab-e1d11cc44315"
  # leave tls_insecure set to true unless you have your proxmox SSL certificate situation fully sorted out (if you do, you will know)
  pm_tls_insecure = true
}

