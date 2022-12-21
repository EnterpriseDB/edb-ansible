include ../../Makefile.mk

build-centos7:
	docker compose up primary1-centos7 -d
	docker compose up standby1-centos7 -d
	docker compose up standby2-centos7 -d
	docker compose up pgbackrest1-centos7 -d

build-rocky8:
	docker compose up primary1-rocky8 -d
	docker compose up standby1-rocky8 -d
	docker compose up standby2-rocky8 -d
	docker compose up pgbackrest1-rocky8 -d

build-debian10:
	docker compose up primary1-debian10 -d
	docker compose up standby1-debian10 -d
	docker compose up standby2-debian10 -d
	docker compose up pgbackrest1-debian10 -d

build-ubuntu20:
	docker compose up primary1-ubuntu20 -d
	docker compose up standby1-ubuntu20 -d
	docker compose up standby2-ubuntu20 -d
	docker compose up pgbackrest1-ubuntu20 -d
