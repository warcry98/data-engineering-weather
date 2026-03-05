FROM kestra/kestra:latest

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# install python libs
RUN pip3 install \
    dlt \
    aiohttp \
    psycopg2-binary \
    boto3

# install bruin CLI
RUN curl -L https://github.com/bruin-data/bruin/releases/latest/download/bruin-linux-amd64 \
    -o /usr/local/bin/bruin \
    && chmod +x /usr/local/bin/bruin

# install awscli
RUN pip3 install awscli

WORKDIR /app