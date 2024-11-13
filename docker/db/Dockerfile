## TODO
## docker compose setting require

## Require : DataBase install
## Require : docker exporter install
## 0.2

FROM mariadb:latest
WORKDIR /download

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    vim

COPY init/init.sql /docker-entrypoint-initdb.d/