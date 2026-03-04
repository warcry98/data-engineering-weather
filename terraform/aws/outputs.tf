resource "aws_ssm_document" "add_ssh_key" {
  name          = "AddUbuntuSSHKey"
  document_type = "Command"

  content = jsonencode({
    schemaVersion = "2.2"
    description   = "Add SSH public key to ubuntu authorized_keys"
    mainSteps = [{
      action = "aws:runShellScript"
      name   = "addKey"
      inputs = {
        runCommand = [
          "install -d -m 700 /home/ubuntu/.ssh",
          "echo '${var.ssh_public_key}' >> /home/ubuntu/.ssh/authorized_keys",
          "chown -R ubuntu:ubuntu /home/ubuntu/.ssh",
          "chmod 600 /home/ubuntu/.ssh/authorized_keys"
        ]
      }
    }]
  })
}

resource "aws_ssm_association" "add_ssh_key" {
  name = aws_ssm_document.add_ssh_key.name

  targets {
    key    = "InstanceIds"
    values = [aws_instance.this.id]
  }
}