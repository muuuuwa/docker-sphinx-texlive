FROM ubuntu:16.04

RUN apt-get update && apt-get install -y -q \
  build-essential \
  python3-dev \
  python3-pip \
  libjpeg8-dev \
  zlib1g-dev \
  libtiff5-dev \
  libfreetype6-dev \
  fonts-takao \
  fonts-vlgothic \
  texlive-full

RUN mkdir /docs/
WORKDIR /docs/


RUN mkdir /src/
ENV PYTHONPATH /src

COPY requirements.txt /docs/
RUN pip3 install -r requirements.txt

CMD export LC_ALL=C.UTF-8; alias python=python3; make latexpdf
