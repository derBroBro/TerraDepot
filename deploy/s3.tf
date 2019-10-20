resource "aws_s3_bucket" "state_bucket" {
  bucket = "${var.name}-store"
  acl    = "private"

  versioning {
    enabled = true
  }
}
