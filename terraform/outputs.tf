output "ecr_repo_url" { value = aws_ecr_repository.app.repository_url }
output "tools_public_ip" { value = aws_instance.tools.public_ip }
output "eks_name" { value = aws_eks_cluster.main.name }
