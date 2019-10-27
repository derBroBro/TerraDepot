output "url"{
      value = local.url
}
output "example_usage"{
      value = <<EOT
terraform {
  backend "http" {
    address = "${local.url}/project/someproject?key=d9823a09d923aud9"
  }
}
EOT

}

output "hint"{
    value = local.hint
}
