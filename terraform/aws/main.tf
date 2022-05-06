resource "aws_instance" "cerberus" {
  ami = var.ami
  instance_type = var.instance_type
  key_name   = "cerberus"
  user_data = file("install-nginx.sh")
}
resource "aws_key_pair" "cerberus-key" {
  key_name   = "cerberus"
  public_key = file(".ssh/cerberus.pub")
}
resource "aws_eip" "eip" {
  instance = aws_instance.cerberus.id
  vpc      = true
  provisioner "local-exec" {
    command = "echo ${self.public_dns} >> /root/cerberus_public_dns.txt"
  }
}