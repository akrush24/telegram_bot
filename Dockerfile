FROM ubuntu:latest
ADD requirements.txt /home/
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
&& apt-get install -yq python3-pip wkhtmltopdf xvfb \
&& rm -rf /var/lib/apt/lists/*
RUN pip3 install -r /home/requirements.txt
#CMD [ "/home/bot.py" ]
