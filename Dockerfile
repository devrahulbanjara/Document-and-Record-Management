FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    git

WORKDIR template

COPY . .

RUN pip install .[dev]

CMD ["/bin/bash/"]
