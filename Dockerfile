FROM continuumio/miniconda3

RUN apt-get update
RUN apt-get install -y gcc python3-dev python3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app/

ENTRYPOINT "/bin/bash"