include ../../Makefile.mk

build-rocky8:
	docker compose up primary1-rocky8 -d
	docker compose up standby1-rocky8 -d
	docker compose up standby2-rocky8 -d
	docker compose up pooler1-rocky8 -d

build-rocky9:
	docker compose up primary1-rocky9 -d
	docker compose up standby1-rocky9 -d
	docker compose up standby2-rocky9 -d
	docker compose up pooler1-rocky9 -d

build-centos7:
	docker compose up primary1-centos7 -d
	docker compose up standby1-centos7 -d
	docker compose up standby2-centos7 -d
	docker compose up pooler1-centos7 -d

build-almalinux8:
	docker compose up primary1-almalinux8 -d
	docker compose up standby1-almalinux8 -d
	docker compose up standby2-almalinux8 -d
	docker compose up pooler1-almalinux8 -d
