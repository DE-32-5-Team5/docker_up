## TODO
## Docker compose setting - blog

## Require : Grafana install
## Require : app.py - Homepage
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
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

# Streamlit 기본 포트
EXPOSE 8501

# Streamlit의 health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "headless = true"]
