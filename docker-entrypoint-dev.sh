#!/bin/sh

cd /app
apt-get install xdotool -y
rm -rf /var/run/pulse /var/lib/pulse /root/.config/pulse
pulseaudio -D --verbose --exit-idle-time=-1 --system --disallow-exit
pactl load-module module-virtual-sink sink_name=v1
pactl set-default-sink v1
pactl set-default-source v1.monitor



./recorder.sh


aws s3 cp out.mp3 $BUCKET_PRESET/$UUID.mp3

if [ -f start.txt ] && [ -f out.mp3 ]; then
    python3 done.py
fi
