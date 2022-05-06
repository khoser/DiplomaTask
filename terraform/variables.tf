variable "token" {
  description = "token data"
  type = map
  default = {
    "id" = ""
    "key" = ""
  }
}

variable "tkn" {
  description = "token data"
  type = object({
    id = string
    key = string
  })
  default = {
    id = ""
    key = ""
  }
}

