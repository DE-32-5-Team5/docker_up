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
[+] Running 6/6
 ✔ Network oneshot_default         Created                                                                                                                           0.1s
 ✔ Container mariadb_container     Started                                                                                                                           0.7s
 ✔ Container oneshot-controller-1  Started                                                                                                                           0.9s
 ✔ Container oneshot-agent-1       Started                                                                                                                           1.4s
 ✔ Container oneshot-blog-1        Started                                                                                                                           1.3s
 ✔ Container oneshot-ng-1          Started
```

``` bash
# manual installation

$ docker compose up -d -f docker-compose.yml -f ng-compose.yml --force-rec

[+] Running 5/5
 ✔ Network team5_default            Created                                                     0.2s
 ✔ Container team5-blog-1           Started                                                     1.5s
 ✔ Container team5-controller-1     Started                                                     0.9s
 ✔ Container team5-load_balancer-1  Started                                                     1.9s
 ✔ Container team5-agent-1          Started                                                     1.1s
```
### Containers remove
``` bash
$ oneshot -d
[+] Running 6/6
 ✔ Container oneshot-agent-1       Removed                                                                                                                          10.5s
 ✔ Container oneshot-ng-1          Removed                                                                                                                           2.6s
 ✔ Container oneshot-blog-1        Removed                                                                                                                           1.7s
 ✔ Container mariadb_container     Removed                                                                                                                           3.7s
 ✔ Container oneshot-controller-1  Removed                                                                                                                          12.7s
 ✔ Network oneshot_default         Removed 
```
## Usage

