#!/bin/bash
sudo docker run --restart always -d -h tbot --name tbot -v /home/akrush/python/telegram/:/home/akrush/python/telegram akrush/tbot:v6
