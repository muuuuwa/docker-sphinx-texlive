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

RUN apt-get update && apt-get install -y -q \
  git

RUN mkdir /docs/
WORKDIR /docs/
COPY requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt
RUN pip3 install requests boto3

RUN mkdir /opt2/

COPY upload_pdf.py /opt/
#CMD export LC_ALL=C.UTF-8; alias python=python3; git clone ${REPO_URL} /docs/ ; make latexpdf; python3 /opt/upload_pdf.py
CMD export LC_ALL=C.UTF-8; alias python=python3; git clone ${REPO_URL} -b ${BRANCH} --depth 1 /docs/ > /tmp/document_build.log 2>&1; make latexpdf >> /tmp/document_build.log 2>&1; python3 /opt/upload_pdf.py
