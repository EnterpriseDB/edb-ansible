ansible-tester-up:
	docker compose up ansible-tester --force-recreate --build --abort-on-container-exit --exit-code-from ansible-tester

post-build:
	python3 ../../scripts/ssh-keygen.py --ssh-dir .ssh
	python3 ../../scripts/prep-containers.py --compose-dir . --ssh-dir .ssh
	python3 ../../scripts/build-inventory.py --compose-dir .
	python3 ../../scripts/ssh-build-add-hosts-sh.py --compose-dir . --ssh-dir .ssh
	python3 ../../scripts/ssh-build-ssh-config.py --ssh-dir .ssh

centos7: export EDB_OS=centos7
centos8: export EDB_OS=centos8
rocky8: export EDB_OS=rocky8
rocky9: export EDB_OS=rocky9
rhel8: export EDB_OS=rhel8
almalinux8: export EDB_OS=almalinux8
debian9: export EDB_OS=debian9
debian10: export EDB_OS=debian10
debian11: export EDB_OS=debian11
ubuntu20: export EDB_OS=ubuntu20
ubuntu22: export EDB_OS=ubuntu22
suse15: export EDB_OS=suse15
oraclelinux7: export EDB_OS=oraclelinux7
oraclelinux8: export EDB_OS=oraclelinux8
oraclelinux9: export EDB_OS=oraclelinux9

centos7: build-centos7 post-build ansible-tester-up
centos8: build-centos8 post-build ansible-tester-up
rocky8: build-rocky8 post-build ansible-tester-up
rocky9: build-rocky9 post-build ansible-tester-up
rhel8: build-rhel8 post-build ansible-tester-up
almalinux8: build-almalinux8 post-build ansible-tester-up
debian9: build-debian9 post-build ansible-tester-up
debian10: build-debian10 post-build ansible-tester-up
debian11: build-debian11 post-build ansible-tester-up
ubuntu20: build-ubuntu20 post-build ansible-tester-up
ubuntu22: build-ubuntu22 post-build ansible-tester-up
suse15: build-suse15 post-build ansible-tester-up
oraclelinux7: build-oraclelinux7 post-build ansible-tester-up
oraclelinux8: build-oraclelinux8 post-build ansible-tester-up
oraclelinux9: build-oraclelinux9 post-build ansible-tester-up

clean:
	rm -rf ./.ssh
	rm -f ./inventory.yml
	docker compose rm -s -f
