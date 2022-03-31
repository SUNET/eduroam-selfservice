FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt update
RUN apt install -y git supervisor emacs-nox virtualenv procps python3 python3-pip
RUN apt clean

RUN mkdir /opt/selfservice

COPY . /opt/selfservice/
COPY supervisord.conf /etc/supervisor/

WORKDIR /opt/selfservice/
RUN pip3 install -r requirements.txt

ENTRYPOINT supervisord -c /etc/supervisor/supervisord.conf
