# fhriley/mediaelch

Container for MediaElch (http://www.kvibes.de/mediaelch/)

Run MediaElch with the GUI available over HTTP or VNC.

https://hub.docker.com/r/fhriley/mediaelch

https://github.com/fhriley/mediaelch-docker

**This image will run natively on Raspberry Pi and MacOS**

## Usage

```bash
docker run --name=mediaelch \
  -d --init \
  -v $PWD/data:/data \
  -v $PWD/movies:/media/movies \
  -v $PWD/tv:/media/tv \
  -e TZ=America/New_York \
  -e MEDIAELCH_UID=2000 \
  -e MEDIAELCH_GID=2000 \
  -p 5900:5900/tcp \
  -p 8000:8000/tcp \
  fhriley/mediaelch
```

Docker compose example:

```yaml
version: "3"

services:
  kodi:
   image: fhriley/mediaelch
   restart: always
   init: true
   ports:
     - "5900:5900/tcp"
     - "8000:8000/tcp"
   environment:
     MEDIAELCH_UID: 2000
     MEDIAELCH_GID: 2000
     TZ: America/New_York
   volumes:
     - ./data:/data
     - ./movies:/media/movies
     - ./tv:/media/tv 
```

**Ports**

* `5900/tcp` - VNC port
* `8000/tcp` - noVNC HTTP port

**Volumes**

* `/data` - path for MediaElch data and configuration files
* `/media/movies` - path for movies
* `/media/tv` - path for tv shows

**Environment Variables**

* `MEDIAELCH_UID` - The user ID to run all processes in the container under (default `2000`)
* `MEDIAELCH_GID` - The group ID to run all processes in the container under (default `2000`)
* `TZ` - The timezone to use in the container (default `UTC`)

## Tags

| Tagname  | Version  | Base distro | Architecture         |
|----------|---------|--------------|----------------------|
| `latest` | 2.8.14  | Ubuntu 22.04 | amd64, armv7, arm64  |
| `2.8.14` | 2.8.14  | Ubuntu 22.04 | amd64, armv7, arm64  |

Docker will automatically pull the correct architecture for your platform.

## User / Group Identifiers

The volumes must be readable and writable by the user ID that you run the container under.
