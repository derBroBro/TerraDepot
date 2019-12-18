data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "state_bucket" {
  bucket = "${data.aws_caller_identity.current.account_id}-${var.name}"
  acl    = "private"

  versioning {
    enabled = true
  }
}
