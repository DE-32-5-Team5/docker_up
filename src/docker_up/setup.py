import sys
import argparse
import subprocess
import os

def main():
  parser = argparse.ArgumentParser(description='BCS 도움말', add_help=False)
  parser.add_argument('-h', '--help', action='store_true', help='도움말 표시')
  parser.add_argument('-i', '--init', action='store_true', help='패키지 설치')
  args = parser.parse_args()
  if args.help:
    print("""
	Playdata Encore Data Engineering 32rd 
	5th Team's 4th Project

	Docker_up
	version 0.2.0

	This Project is practice project that learn skills about docker-compose and consider project architecture that our final project. 
	This package make 3 docker-containers in your local system. each container named blog, nginx, db.

	Blog container include Grafana dashboard system and our Homepage using streamlit.
	Nginx container include Promtheus overwatch system and ab : stress test system.
	DB container include MariaDB and Docker-exporter pointer system.

	Commands
	oneshot, oneshot -h, --help		: Show command help screen
	                 -i, --init		: Install Docker Containers 
	

	"""
	)
  elif args.init:
    try:
      subprocess.run(['docker', 'compose', 'up', '-d'], check=True)
    except subprocess.CalledProcessError as e:
      print(f"오류 발생: {e}")
      print("docker-compose 명령어 실행에 실패했습니다. Docker Compose가 설치되어 있는지 확인해주세요.")


if __name__ == '__main__':
  main()
