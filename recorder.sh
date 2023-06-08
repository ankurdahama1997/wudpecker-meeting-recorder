#!/bin/bash
trap 'kill $(pgrep ffmpeg)' SIGTERM SIGINT


echo "recorder.sh"
# Start ffmpeg in the background, taking input from the named pipe
./audio.sh&

echo "Attempting to start XVFB..."
outp=$(xvfb-run --server-args="-screen 0 1024x768x24" python3 bot.py)
echo "${outp}"

echo "Turning off the FFMPEG now"

kill $(pgrep ffmpeg)
exit
