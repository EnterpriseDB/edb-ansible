#!/bin/bash -eux
mkdir -p /root/.ssh
chmod 0700 /root/.ssh
cp "/workspace/cases/${CASE_NAME}/.ssh/id_rsa" /root/.ssh/.
cp "/workspace/cases/${CASE_NAME}/.ssh/ssh_config" /root/.ssh/.
chmod 0600 /root/.ssh/id_rsa
"/workspace/cases/${CASE_NAME}/.ssh/add_hosts.sh"

export ANSIBLE_CONFIG=/workspace/docker/ansible.cfg
ansible-playbook \
	-i "/workspace/cases/${CASE_NAME}/inventory.yml" \
	--extra-vars "pg_type=${OPENSQL_PG_TYPE}" \
	--extra-vars "pg_version=${OPENSQL_PG_VERSION}" \
	--extra-vars "@/workspace/cases/${CASE_NAME}/vars.json" \
	--private-key /root/.ssh/id_rsa \
	"/workspace/cases/${CASE_NAME}/playbook.yml"

export OPENSQL_SSH_USER=root
export OPENSQL_SSH_KEY=/root/.ssh/id_rsa
export OPENSQL_SSH_CONFIG=/root/.ssh/ssh_config
export OPENSQL_INVENTORY="/workspace/cases/${CASE_NAME}/inventory.yml"
export OPENSQL_ANSIBLE_VARS="/workspace/cases/${CASE_NAME}/vars.json"

py.test -v -k "${CASE_NAME}" /workspace/tests
