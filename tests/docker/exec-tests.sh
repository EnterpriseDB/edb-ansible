#!/bin/bash -eux
cd /workspace
make install-build
mkdir -p /root/.ssh
chmod 0700 /root/.ssh
cp /workspace/tests/cases/${CASE_NAME}/.ssh/id_rsa /root/.ssh/.
cp /workspace/tests/cases/${CASE_NAME}/.ssh/ssh_config /root/.ssh/.
chmod 0600 /root/.ssh/id_rsa
/workspace/tests/cases/${CASE_NAME}/.ssh/add_hosts.sh
ANSIBLE_PIPELINING=1 ansible-playbook \
	-i /workspace/tests/cases/${CASE_NAME}/inventory.yml \
	--extra-vars "repo_username=${EDB_REPO_USERNAME}" \
	--extra-vars "repo_password=${EDB_REPO_PASSWORD}" \
	--extra-vars "repo_token=${EDB_REPO_TOKEN}" \
	--extra-vars "enable_edb_repo=${EDB_ENABLE_REPO}" \
	--extra-vars "pg_type=${EDB_PG_TYPE}" \
	--extra-vars "pg_version=${EDB_PG_VERSION}" \
	--extra-vars "@/workspace/tests/cases/${CASE_NAME}/vars.json" \
	--extra-vars "ansible_core_version=${ANSIBLE_CORE_VERSION}" \
	--private-key /root/.ssh/id_rsa \
	/workspace/tests/cases/${CASE_NAME}/playbook.yml

export EDB_SSH_USER=root
export EDB_SSH_KEY=/root/.ssh/id_rsa
export EDB_SSH_CONFIG=/root/.ssh/ssh_config
export EDB_INVENTORY=/workspace/tests/cases/${CASE_NAME}/inventory.yml
export EDB_ANSIBLE_VARS=/workspace/tests/cases/${CASE_NAME}/vars.json
py.test -v -k ${CASE_NAME} /workspace/tests/tests
