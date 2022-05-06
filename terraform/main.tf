resource "local_file" "temp" {
  filename = "./temp.txt"
  content = "some text"
}

resource "local_sensitive_file" "token" {
  filename = "./token.data"
  content = "481e2c4a-a0b0-48c1-baab-e1d11cc44315"
  file_permission = "0644"
}
