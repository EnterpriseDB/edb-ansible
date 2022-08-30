ansible-tester-up:
	docker compose up ansible-tester --abort-on-container-exit --exit-code-from ansible-tester

post-build:
	python3 ../../scripts/ssh-keygen.py --ssh-dir .ssh
	python3 ../../scripts/prep-containers.py --compose-dir . --ssh-dir .ssh
	python3 ../../scripts/build-inventory.py --compose-dir .
	python3 ../../scripts/ssh-build-add-hosts-sh.py --compose-dir . --ssh-dir .ssh
	python3 ../../scripts/ssh-build-ssh-config.py --ssh-dir .ssh

centos7: export EDB_OS=centos7
rocky8: export EDB_OS=rocky8
debian9: export EDB_OS=debian9
debian10: export EDB_OS=debian10
ubuntu20: export EDB_OS=ubuntu20
oraclelinux7: export EDB_OS=oraclelinux7

centos7: build-centos7 post-build ansible-tester-up
rocky8: build-rocky8 post-build ansible-tester-up
debian9: build-debian9 post-build ansible-tester-up
debian10: build-debian10 post-build ansible-tester-up
ubuntu20: build-ubuntu20 post-build ansible-tester-up
oraclelinux7: build-oraclelinux7 post-build ansible-tester-up

clean:
	rm -rf ./.ssh
	rm -f ./inventory.yml
	docker compose rm -s -f
