ARG BASE_IMAGE="fhriley/vnc-base:latest"
FROM $BASE_IMAGE

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y \
    software-properties-common \
    icewm \
  && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

RUN add-apt-repository -y ppa:mozillateam/ppa \
  && apt-get update \
  && apt-get install -y -t 'o=LP-PPA-mozillateam' firefox \
  && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

COPY supervisord.conf /supervisor.d/
COPY icewm /etc/X11/icewm
COPY entrypoint.sh /entrypoint.d/

VOLUME /config

ENV VNC_UID=1000
ENV VNC_GID=1000
ENV VNC_WINDOW_NAME=Firefox
