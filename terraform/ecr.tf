ecr.tf

resource "aws_ecr_repository" "app" {
  name = "${var.project}-app"
  image_scanning_configuration { scan_on_push = true }
}
