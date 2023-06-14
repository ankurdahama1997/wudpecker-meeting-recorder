#!/bin/bash

echo "Checking for xvfb..."
x=1
while :
do
    echo "checking..."
    if ps -ef | grep Xvfb | grep -v 'grep' | grep -q 'auth'; then
        echo "DISPLAY FOUND"
        break
    else
        echo "output"
        sleep 1
    fi
done


out=$(ps -ef | grep Xvfb)

export XAUTHORITY=$(python3 xauthsplit.py "$out")



# Wait for the start.txt file to be created
echo "Waiting for start.txt to know that bot is accpeted..."
while :
do
    if [ -f start.txt ]; then
        echo "Bot accepted, starting ffmpeg"
        break
    else
        sleep 1
    fi
done



ffmpeg -loglevel error -f "pulse" -i default -y out.mp4