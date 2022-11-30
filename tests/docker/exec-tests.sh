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
	--extra-vars "pg_type=${HYPERSQL_PG_TYPE}" \
	--extra-vars "pg_version=${HYPERSQL_PG_VERSION}" \
	--extra-vars "@/workspace/cases/${CASE_NAME}/vars.json" \
	--private-key /root/.ssh/id_rsa \
	"/workspace/cases/${CASE_NAME}/playbook.yml"

export HYPERSQL_SSH_USER=root
export HYPERSQL_SSH_KEY=/root/.ssh/id_rsa
export HYPERSQL_SSH_CONFIG=/root/.ssh/ssh_config
export HYPERSQL_INVENTORY="/workspace/cases/${CASE_NAME}/inventory.yml"
export HYPERSQL_ANSIBLE_VARS="/workspace/cases/${CASE_NAME}/vars.json"

py.test -v -k "${CASE_NAME}" /workspace/tests
