terraform {
  backend "http" {
    address = "https://czrqnde1f7.execute-api.eu-central-1.amazonaws.com/test/project/malte?key=1234"
  }
}