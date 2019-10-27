locals {
    url = (var.domain != "" ? "https://${var.domain}" : aws_api_gateway_deployment.prod.invoke_url)
    hint = (var.domain != "" ? "Create a CNAME from ${var.domain} to ${aws_api_gateway_domain_name.main.cloudfront_domain_name}" : "")

}