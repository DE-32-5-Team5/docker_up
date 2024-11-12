# Encore PlayData DE32 5th team
# docker_up

## Intrduce

## Installation

``` bash
$ git clone https://github.com/DE-32-5-Team5/docker_up.git
$ cd docker_up
$ git checkout 0.2/release
$ pdm venv create
$ source .venv/bin/activate
$ pip install .
$ oneshot -i
```

``` bash
#manual installation

$ docker compose up -d -f docker-compose.yml -f ng-compose.yml --force-rec

[+] Running 5/5
 ✔ Network team5_default            Created                                                     0.2s
 ✔ Container team5-blog-1           Started                                                     1.5s
 ✔ Container team5-controller-1     Started                                                     0.9s
 ✔ Container team5-load_balancer-1  Started                                                     1.9s
 ✔ Container team5-agent-1          Started                                                     1.1s
```

## Usage

## autoscale
