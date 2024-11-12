## TODO
## Docker compose setting - dashboard 

## Require : Grafana install
FROM python:3.9-slim

WORKDIR /code

COPY ./app.py /code/

# 필수 패키지 및 Grafana 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    adduser \
    libfontconfig1 \
    musl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -O https://dl.grafana.com/oss/release/grafana_11.3.0_amd64.deb \
    && dpkg -i grafana_11.3.0_amd64.deb \
    && rm grafana_11.3.0_amd64.deb

# Grafana 기본 포트
EXPOSE 3000
