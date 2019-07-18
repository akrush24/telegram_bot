#!/bin/bash
sudo docker run --restart always -h tbot:v5 --name tbot -d -v /home/akrush/python/telegram/:/home/ akrush/tbot:v5

