FROM ubuntu:latest
ADD requirements.txt /
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
&& apt-get install -yq python3-pip wkhtmltopdf xvfb \
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install -r /requirements.txt
CMD ["/bin/sh", "-c", "/home/akrush/python/telegram/bot.py >> /home/akrush/python/telegram/bot.py.logs 2>&1" ]
#CMD ["/bin/sh", "-c", "python3 /home/akrush/python/telegram/bot.py > /home/akrush/python/telegram/bot.py.logs 2>&1" ]
