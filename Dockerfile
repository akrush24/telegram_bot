FROM ubuntu:latest
ADD requirements.txt /
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
&& apt-get install -yq python3-pip wkhtmltopdf xvfb git \
&& rm -rf /var/lib/apt/lists/* \
&& pip3 install -r /requirements.txt
RUN git clone https://github.com/akrush24/telegram_bot.git /tbot/
#CMD ["/usr/bin/git", "clone", "https://github.com/akrush24/telegram_bot.git", "/tbot/"]
#CMD ["/bin/sh", "-c", "/tbot/bot.py >> /tbot/bot.py.logs 2>&1" ]
