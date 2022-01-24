job "imageserver" {
    group "imageserver" {
        network {
            port "webserver" {
                to = 8000
            }
        }
        service {
            name = "imageserver"
            tags = ["imageserver", "urlprefix-/"]
            port = "webserver"
            check {
                name     = "alive"
                type     = "http"
                path     = "/"
                interval = "10s"
                timeout  = "2s"
            }
        }
        task "imageserver" {
            driver = "docker"

            config {
                image = "ghcr.io/tag-epic/imageserver/imageserver"

                ports = ["webserver"]
            }

            resources {
                cpu    = 50
                memory = 50
            }

            template {
                data = <<EOF
                    {{ with secret "kv/imageserver" }}
                    ROOT_KEY={{.Data.data.root_key}}
                    ALLOWED_TOKENS={{.Data.data.allowed_tokens}}
                    USE_HTTPS={{.Data.data.use_https}}
                    URL_PREFIX={{.Data.data.url_prefix}}
                    {{ end }}
                EOF
                destination = "local/env"
                env         = true
            }
        }
    }
}
