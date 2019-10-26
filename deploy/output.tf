output "url"{
      value = aws_api_gateway_deployment.prod.invoke_url
}
output "example_usage"{
      value = <<EOT
terraform {
  backend "http" {
    address = "${aws_api_gateway_deployment.prod.invoke_url}/project/someproject?key=d9823a09d923aud9"
  }
}
EOT

}
