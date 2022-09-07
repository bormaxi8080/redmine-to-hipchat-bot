FROM debian:jessie

ENV TERM xterm

WORKDIR /var/www

RUN rm -rf /var/lib/apt/lists* \
&& apt-get update

RUN rm -rf /var/lib/apt/lists* \
&& apt-get update \
&& apt-get install -y python-pip libpq-dev python-dev libffi-dev

COPY run.sh /
RUN chmod +x /run.sh
CMD /run.sh

RUN pip install "tornado>=4.0,<4.1" "python-simple-hipchat" "python-redmine"
