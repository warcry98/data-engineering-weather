output "instance_id" {
  value = aws_instance.this.id
}

output "public_ip" {
  value = aws_instance.this.public_ip
}

output "ssm_connect" {
  value = "aws ssm start-session --target ${aws_instance.this.id}"
}