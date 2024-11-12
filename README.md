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
Initialize env setting...
Enter Database root password : <your root password>
Enter Database Name : <your database>
Enter User Name : <your user name>
Enter user Password : <your user password>
env install complete.
[+] Running 4/4
 ✔ Network oneshot_default      Created                                                                            0.2s
 ✔ Container mariadb_container  Started                                                                            0.6s
 ✔ Container oneshot-blog-1     Started                                                                            0.9s
 ✔ Container oneshot-ng-1       Started 
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

