variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "flask-mysql"
}

variable "tools_instance_type" {
  description = "EC2 instance type for tools server"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}
