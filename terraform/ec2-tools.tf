resource "aws_instance" "tools" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.tools_instance_type
  subnet_id     = aws_subnet.public_a.id
  key_name      = var.key_name

  vpc_security_group_ids = [
    aws_security_group.tools_sg.id
  ]

  user_data = file("${path.module}/userdata/tools.sh")

  root_block_device {
    volume_size           = 100
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "${var.project}-tools"
  }
}

