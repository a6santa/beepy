FROM ubuntu

ENV PYTHONIOENCODING utf-8

RUN apt-get update && \
    apt-get install -y python3 \
	python3-pip \
	python-dev \
	python3-dev \
	build-essential \
	libssl-dev \
	libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libpq-dev \
    unixodbc \
    unixodbc-dev \
    freetds-bin \
    freetds-common \
    freetds-dev \
	git \
	vim \
	autoconf \
	gettext

COPY . /beblue-bi-etls
WORKDIR /beblue-bi-etls

RUN rm -rf /var/lib/apt/lists/*

CMD /bin/bash

RUN pip3 install --upgrade pip
RUN pip3 install -U googlemaps
RUN pip3 install -r requirements.txt

RUN python3 setup.py develop