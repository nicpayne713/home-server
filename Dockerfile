FROM continuumio/miniconda3

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

ENTRYPOINT "/bin/bash"