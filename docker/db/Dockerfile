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

# mysqld_exporter 다운로드
RUN wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.15.1/mysqld_exporter-0.15.1.linux-amd64.tar.gz \
  && tar -xvf mysqld_exporter-0.15.1.linux-amd64.tar.gz \
  && rm mysqld_exporter-0.15.1.linux-amd64.tar.gz

# mysqld_exporter 실행
RUN cd /download/mysqld_exporter-0.15.1.linux-amd64 && ./mysqld_exporter --config.my-cnf=/download/mysqld_exporter-0.15.1.linux-amd64/setting/.my.cnf

