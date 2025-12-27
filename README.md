# nmapp

![](nmapp.gif)

nmapp is a CLI tool which parses Nmap scan output and renders it into a normalized, deterministic Markdown format. Given two logically equivalent Nmap scans—even if they differ in ordering, timing, or extraneous metadata—nmapp produces the same predictable Markdown output.

## Installation

### With pipx

Coming soon

[//]: # (```sh)

[//]: # (pipx install nmapp)

[//]: # (```)


### With uv

Coming soon

[//]: # (```sh)

[//]: # (uv tool install nmapp)

[//]: # (```)

### With docker

```sh
docker run --rm \
  ghcr.io/hacktegic/nmapp:latest nmapp --help
```
