## TODO
## Docker compose setting require

## Require : ngrinder install
## Require : nginx install
## Require : prometheus install
## 0.2

FROM nginx:1.25.1

COPY ["default.conf", "/etc/nginx/conf.d/"]

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    supervisor \
    vim

RUN wget https://github.com/prometheus/prometheus/releases/download/v2.53.3/prometheus-2.53.3.linux-amd64.tar.gz \
  && tar -xvf prometheus-2.53.3.linux-amd64.tar.gz \
  && rm prometheus-2.53.3.linux-amd64.tar.gz

RUN wget https://github.com/naver/ngrinder/releases/download/ngrinder-3.5.9-p1-20240613/ngrinder-controller-3.5.9-p1.war \
  && unzip ngrinder-controller-3.5.9-p1.war \
  && rm ngrinder-controller-3.5.9-p1.war
