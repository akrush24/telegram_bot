FROM ubuntu:latest
ADD requirements.txt dark-theme.css passwd.*.py bot.py /home/
RUN apt-get update \
  && apt-get install -y python3-pip wkhtmltopdf \
  && pip3 install -r requirements.txt \
  && rm -rf /var/lib/apt/lists/*
