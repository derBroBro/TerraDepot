resource "local_file" "test" {
    content     = "foo!"
    filename = "test.txt"
}