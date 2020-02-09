resource "aws_sns_topic" "config_updates" {
  name = "${var.name}_config_updates"
}

resource "aws_sns_topic" "state_updates" {
  name = "${var.name}_state_updates"
}