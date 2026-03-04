variable "aws_region" {
  default = "us-east-1"  
}

variable "allowed_ssh_cidr" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "allowed_kestra_cidr" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "allowed_metabase_cidr" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "allowed_db_cidr" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "instance_name" {
  default = "ubuntu-bmkg-weather"
}

variable "ssh_public_key" {
  description = "SSH public key content"
  type        = string
}