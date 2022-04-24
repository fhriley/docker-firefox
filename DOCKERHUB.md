# Firefox container with display over HTTP and/or VNC

This is a Docker container for [Firefox](https://www.mozilla.org/en-US/firefox/).

The GUI of the application is accessed through a modern web browser (no installation or configuration needed on the client side) or via any VNC client.

For simple use cases, this container is a drop-in replacement for [jlesage/firefox](https://hub.docker.com/r/jlesage/firefox). It improves on that image in the following ways:

1. Support for amd64, armv7, and arm64.
2. The Firefox window will resize to the browser or VNC client.

---

[![Firefox logo](https://images.weserv.nl/?url=raw.githubusercontent.com/jlesage/docker-templates/master/jlesage/images/firefox-icon.png&w=200)](https://www.mozilla.org/en-US/firefox/)[![Firefox](https://dummyimage.com/400x110/ffffff/575757&text=Firefox)](https://www.mozilla.org/en-US/firefox/)

Mozilla Firefox is a free and open-source web browser developed by Mozilla Foundation and its subsidiary, Mozilla Corporation.

---

## Quick Start

**NOTE**: The Docker command provided in this quick start is given as an example
and parameters should be adjusted to your need.

Launch the Firefox docker container with the following command:
```
docker run -d \
    --name=firefox \
    -p 5800:5800 \
    -v /docker/appdata/firefox:/config:rw \
    --shm-size 2g \
    fhriley/firefox
```

Where:
  - `/docker/appdata/firefox`: This is where the application stores its configuration, log and any files needing persistency.

Browse to `http://your-host-ip:5800` to access the Firefox GUI.

## Documentation

Full documentation is available at https://github.com/fhriley/docker-firefox.

## Support or Contact

Having troubles with the container or have questions?  Please
[create a new issue].


[create a new issue]: https://github.com/fhriley/docker-firefox/issues
