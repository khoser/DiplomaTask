#resource "local_file" "temp" {
#  filename = "./temp.txt"
#  content = "some text"
#}
#
#resource "local_sensitive_file" "token" {
#  filename = "./token.data"
#  content = "481e2c4a-a0b0-48c1-baab-e1d11cc44315"
#  file_permission = "0644"
#}


resource "tls_private_key" "connection-key" {
  algorithm = "ED25519"
}

resource "local_sensitive_file" "private_key" {
  filename = "./pk_${formatdate("YYYY-MM-DD-hh-mm-ZZZ", timestamp())}" 
  content  = tls_private_key.connection-key.private_key_openssh
}

resource "local_file" "publick_key" {
  filename = "${local_sensitive_file.private_key.filename}.pub"
  content  = tls_private_key.connection-key.public_key_openssh
}

resource "proxmox_vm_qemu" "database" {
  name        = "db"
  clone       = "ubuntu-cloud-guest"
  agent       = 1
  target_node = "xeon"
  cores       = 1
  memory      = 8192
  os_type     = "cloud-init"
  ipconfig0   = "ip=dhcp"
  disk {
    // This disk will become scsi0
    type    = "scsi"
    storage = "hdd500b"
    size    = "50G"
  }
  disk {
    // This disk will become scsi1
    type    = "scsi"
    storage = "hdd500b"
    size    = "100G"
  }
  onboot  = true
  sshkeys = tls_private_key.connection-key.public_key_openssh
  provisioner "local-exec" {
    command = "echo ${self.name} ${self.default_ipv4_address} >> private_ips.txt"
  }
}


resource "proxmox_vm_qemu" "kube-master" {
  name        = "kube-master"
  clone       = "ubuntu-cloud-guest"
  agent       = 1
  target_node = "xeon"
  cores       = 2
  memory      = 8192
  os_type     = "cloud-init"
  ipconfig0   = "ip=dhcp"
  disk {
    // This disk will become scsi0
    type    = "scsi"
    storage = "local-lvm"
    size    = "50G"
  }
  onboot  = true
  sshkeys = tls_private_key.connection-key.public_key_openssh
  provisioner "local-exec" {
    command = "echo ${self.name} ${self.default_ipv4_address} >> private_ips.txt"
  }
}


resource "proxmox_vm_qemu" "kube-workers" {
  count       = 3
  name        = "kube-worker-${count.index + 1}"
  clone       = "ubuntu-cloud-guest"
  agent       = 1
  target_node = "xeon"
  cores       = 3
  memory      = 8192
  os_type     = "cloud-init"
  ipconfig0   = "ip=dhcp"
  disk {
    // This disk will become scsi0
    type    = "scsi"
    storage = "hdd500a"
    size    = "50G"
  }
  onboot  = true
  sshkeys = tls_private_key.connection-key.public_key_openssh
  provisioner "local-exec" {
    command = "echo ${self.name} ${self.default_ipv4_address} >> private_ips.txt"
  }
}

