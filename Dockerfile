# Dockerfile
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev
RUN mkdir -p /app
WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install wget -y
RUN DEBIAN_FRONTEND=noninteractive wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN DEBIAN_FRONTEND=noninteractive apt-get install ./google-chrome-stable_current_amd64.deb -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install xvfb -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install xorg -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install x11vnc -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install xdotool -y

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN DEBIAN_FRONTEND=noninteractive rm google-chrome-stable_current_amd64.deb
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install ffmpeg -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install gpac -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y pulseaudio
RUN adduser root pulse-access

