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

## Table of Content

   * [Docker container for Firefox](#docker-container-for-firefox)
      * [Table of Content](#table-of-content)
      * [Quick Start](#quick-start)
      * [Usage](#usage)
         * [Environment Variables](#environment-variables)
         * [Data Volumes](#data-volumes)
         * [Ports](#ports)
         * [Changing Parameters of a Running Container](#changing-parameters-of-a-running-container)
      * [Docker Compose File](#docker-compose-file)
      * [Docker Image Update](#docker-image-update)
         * [Synology](#synology)
         * [unRAID](#unraid)
      * [User/Group IDs](#usergroup-ids)
      * [Accessing the GUI](#accessing-the-gui)
      * [Shell Access](#shell-access)
      * [Increasing Shared Memory Size](#increasing-shared-memory-size)
      * [Allowing the membarrier System Call](#allowing-the-membarrier-system-call)
      * [Sound Support](#sound-support)
      * [Setting Firefox Preferences Via Environment Variables](#setting-firefox-preferences-via-environment-variables)
      * [Troubleshooting](#troubleshooting)
         * [Crashes](#crashes)
      * [Support or Contact](#support-or-contact)
      * [Credits](#credits)

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

## Usage

```
docker run [-d] \
    --name=firefox \
    [-e <VARIABLE_NAME>=<VALUE>]... \
    [-v <HOST_DIR>:<CONTAINER_DIR>[:PERMISSIONS]]... \
    [-p <HOST_PORT>:<CONTAINER_PORT>]... \
    --shm-size VALUE \
    fhriley/firefox
```
| Parameter | Description |
|-----------|-------------|
| -d        | Run the container in the background.  If not set, the container runs in the foreground. |
| -e        | Pass an environment variable to the container.  See the [Environment Variables](#environment-variables) section for more details. |
| -v        | Set a volume mapping (allows to share a folder/file between the host and the container).  See the [Data Volumes](#data-volumes) section for more details. |
| -p        | Set a network port mapping (exposes an internal container port to the host).  See the [Ports](#ports) section for more details. |
| --shm-size | Set the size of `/dev/shm` to `VALUE`.  The format of `VALUE` is `<number><unit>`, where `number` must be greater than `0` and `unit` can be `b` (bytes), `k` (kilobytes), `m` (megabytes), or `g` (gigabytes).  **NOTE**: To avoid crashes, it is recommended to set this value to `2g`. |

### Environment Variables

To customize some properties of the container, the following environment
variables can be passed via the `-e` parameter (one for each variable).  Value
of this parameter has the format `<VARIABLE_NAME>=<VALUE>`.

| Variable       | Description                                  | Default |
|----------------|----------------------------------------------|---------|
|`USER_ID`| ID of the user the application runs as.  See [User/Group IDs](#usergroup-ids) to better understand when this should be set. | `1000` |
|`GROUP_ID`| ID of the group the application runs as.  See [User/Group IDs](#usergroup-ids) to better understand when this should be set. | `1000` |
|`TZ`| [TimeZone] of the container.  Timezone can also be set by mapping `/etc/localtime` between the host and the container. | `Etc/UTC` |

### Data Volumes

The following table describes data volumes used by the container.  The mappings
are set via the `-v` parameter.  Each mapping is specified with the following
format: `<HOST_DIR>:<CONTAINER_DIR>[:PERMISSIONS]`.

| Container path  | Permissions | Description |
|-----------------|-------------|-------------|
|`/config`| rw | This is where the application stores its configuration, log and any files needing persistency. |

### Ports

Here is the list of ports used by the container.  They can be mapped to the host
via the `-p` parameter (one per port mapping).  Each mapping is defined in the
following format: `<HOST_PORT>:<CONTAINER_PORT>`.  The port number inside the
container cannot be changed, but you are free to use any port on the host side.

| Port | Mapping to host | Description |
|------|-----------------|-------------|
| 5800 | Mandatory | Port used to access the application's GUI via the web interface. |
| 5900 | Optional | Port used to access the application's GUI via the VNC protocol.  Optional if no VNC client is used. |

### Changing Parameters of a Running Container

As can be seen, environment variables, volume and port mappings are all specified
while creating the container.

The following steps describe the method used to add, remove or update
parameter(s) of an existing container.  The general idea is to destroy and
re-create the container:

  1. Stop the container (if it is running):
```
docker stop firefox
```
  2. Remove the container:
```
docker rm firefox
```
  3. Create/start the container using the `docker run` command, by adjusting
     parameters as needed.

**NOTE**: Since all application's data is saved under the `/config` container
folder, destroying and re-creating a container is not a problem: nothing is lost
and the application comes back with the same state (as long as the mapping of
the `/config` folder remains the same).

## Docker Compose File

Here is an example of a `docker-compose.yml` file that can be used with
[Docker Compose](https://docs.docker.com/compose/overview/).

Make sure to adjust according to your needs.  Note that only mandatory network
ports are part of the example.

```yaml
version: '3'
services:
  firefox:
    image: fhriley/firefox
    ports:
      - "5800:5800"
    volumes:
      - "/docker/appdata/firefox:/config:rw"
```

## Docker Image Update

Because features are added, issues are fixed, or simply because a new version
of the containerized application is integrated, the Docker image is regularly
updated.  Different methods can be used to update the Docker image.

The system used to run the container may have a built-in way to update
containers.  If so, this could be your primary way to update Docker images.

An other way is to have the image be automatically updated with [Watchtower].
Watchtower is a container-based solution for automating Docker image updates.
This is a "set and forget" type of solution: once a new image is available,
Watchtower will seamlessly perform the necessary steps to update the container.

Finally, the Docker image can be manually updated with these steps:

  1. Fetch the latest image:
```
docker pull fhriley/firefox
```
  2. Stop the container:
```
docker stop firefox
```
  3. Remove the container:
```
docker rm firefox
```
  4. Create and start the container using the `docker run` command, with the
the same parameters that were used when it was deployed initially.

[Watchtower]: https://github.com/containrrr/watchtower

### Synology

For owners of a Synology NAS, the following steps can be used to update a
container image.

  1.  Open the *Docker* application.
  2.  Click on *Registry* in the left pane.
  3.  In the search bar, type the name of the container (`fhriley/firefox`).
  4.  Select the image, click *Download* and then choose the `latest` tag.
  5.  Wait for the download to complete.  A  notification will appear once done.
  6.  Click on *Container* in the left pane.
  7.  Select your Firefox container.
  8.  Stop it by clicking *Action*->*Stop*.
  9.  Clear the container by clicking *Action*->*Reset* (or *Action*->*Clear* if
      you don't have the latest *Docker* application).  This removes the
      container while keeping its configuration.
  10. Start the container again by clicking *Action*->*Start*. **NOTE**:  The
      container may temporarily disappear from the list while it is re-created.

### unRAID

For unRAID, a container image can be updated by following these steps:

  1. Select the *Docker* tab.
  2. Click the *Check for Updates* button at the bottom of the page.
  3. Click the *update ready* link of the container to be updated.

## User/Group IDs

When using data volumes (`-v` flags), permissions issues can occur between the
host and the container.  For example, the user within the container may not
exist on the host.  This could prevent the host from properly accessing files
and folders on the shared volume.

To avoid any problem, you can specify the user the application should run as.

This is done by passing the user ID and group ID to the container via the
`USER_ID` and `GROUP_ID` environment variables.

To find the right IDs to use, issue the following command on the host, with the
user owning the data volume on the host:

    id <username>

Which gives an output like this one:
```
uid=1000(myuser) gid=1000(myuser) groups=1000(myuser),4(adm),24(cdrom),27(sudo),46(plugdev),113(lpadmin)
```

The value of `uid` (user ID) and `gid` (group ID) are the ones that you should
be given the container.

## Accessing the GUI

Assuming that container's ports are mapped to the same host's ports, the
graphical interface of the application can be accessed via:

  * A web browser:
```
http://<HOST IP ADDR>:5800
```

  * Any VNC client:
```
<HOST IP ADDR>:5900
```

## Shell Access

To get shell access to the running container, execute the following command:

```
docker exec -ti CONTAINER sh
```

Where `CONTAINER` is the ID or the name of the container used during its
creation (e.g. `crashplan-pro`).

## Increasing Shared Memory Size

To prevent crashes from happening when running Firefox
inside a Docker container, the size of the shared memory located at `/dev/shm`
must be increased.  The issue is documented [here].

By default, the size is 64MB, which is not enough.  It is recommended to use a
size of 2GB.  This value is arbitrary, but known to work well.  Setting the
size of `/dev/shm` can be done via two method:

  - By adding the `--shm-size 2g` parameter to the `docker run` command.  See
    the [Usage](#usage) section for more details.
  - By using shared memory of the host, by mapping `/dev/shm` via the parameter
    `-v /dev/shm:/dev/shm` of the `docker run` command.

## Allowing the membarrier System Call

To properly work, recent versions of Firefox need the
`membarrier` system call.  Without it, tabs would frequently crash.

Docker uses [seccomp profile] to restrict system calls available to the
container.  Before Docker version `20.10.0`, the `membarrier` system call was
not allowed in the default profile.  If you run a such version, you can use one
of the following solutions, from the most to the least secure, to provide the
container permission to use this sytem call:

  1. Run the container with a custom seccomp profile allowing the `membarrier`
     system call.  The [latest official seccomp profile] can be used.  Download
     the file and then add the following parameter when creating the container:
     `--security-opt seccomp=/path/to/seccomp_profile.json`.
  2. Run the container without the default seccomp profile (thus allowing all
     system calls). Use the following parameter when creating the container:
     `--security-opt seccomp=unconfined`.
  3. Run the container in privileged mode.  This effectively disables usage of
     seccomp.  Add the `--privileged` parameter when creating the container.

## Sound Support

For Firefox to be able to use the audio device available on
the host, `/dev/snd` must be exposed to the container by adding the
`--device /dev/snd` parameter to the `docker run` command.

## Setting Firefox Preferences Via Environment Variables

Firefox preferences can be set via environment variables
passed to the container.  During the startup, a script process all these
variables and modify the preference file accordingly.

The name of the environment variable must start with `FF_PREF_`, followed by a
string of your choice.  For example, `FF_PREF_MY_PREF` is a valid name.

The content of the variable should be in the format `NAME=VAL`, where `NAME` is
the name of the preference (as found in the `about:config` page) and `VAL` is
its value.  A value can be one of the following types:
  - string
  - integer
  - boolean

It is important to note that a value of type `string` should be surrounded by
double quotes.  Other types don't need them.

For example, to set the `network.proxy.http` preference, one would pass the
environment variable to the container by adding the following argument to the
`docker run` command:

```
-e "FF_PREF_HTTP_PROXY=network.proxy.http=\"proxy.example.com\""
```

If a preference needs to be *removed*, its value should be set to `UNSET`.  For
example:

```
-e "FF_PREF_HTTP_PROXY=network.proxy.http=UNSET"
```

**NOTE**: This is an advanced usage and it is recommended to set preferences
via Firefox directly.

## Troubleshooting

### Crashes

If Firefox is crashing frequently, make sure that:
  - The size of the shared memory located at `/dev/shm` has been increased.  See
    the [Increasing Shared Memory Size](#increasing-shared-memory-size) section
    for more details.
  - The `membarrier` system call is not blocked by Docker.  See the
    [Allowing the membarrier System Call](#allowing-the-membarrier-system-call)
    for more details.
  - Make sure the kernel of your Linux distribution is up-to-date.

[TimeZone]: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones
[here]: https://bugzilla.mozilla.org/show_bug.cgi?id=1338771#c10
[seccomp profile]: https://docs.docker.com/engine/security/seccomp/
[latest official seccomp profile]: https://github.com/moby/moby/blob/master/profiles/seccomp/default.json

## Support or Contact

Having troubles with the container or have questions?  Please
[create a new issue].

[create a new issue]: https://github.com/fhriley/docker-firefox/issues

## Credits

Thanks to [jlesage](https://github.com/jlesage/) for writing an excellent README.
