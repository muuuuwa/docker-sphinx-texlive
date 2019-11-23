FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

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
  fonts-noto-cjk-extra \
  texlive-full

RUN mkdir /docs/
WORKDIR /docs/
COPY requirements.txt /docs/
RUN pip3 install -r requirements.txt

CMD export LC_ALL=C.UTF-8; alias python=python3; make latexpdf
