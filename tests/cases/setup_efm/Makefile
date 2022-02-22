include ../../Makefile.mk

build-centos7:
	docker compose up primary1-centos7 -d
	docker compose up standby1-centos7 -d
	docker compose up standby2-centos7 -d

build-rocky8:
	docker compose up primary1-rocky8 -d
	docker compose up standby1-rocky8 -d
	docker compose up standby2-rocky8 -d
