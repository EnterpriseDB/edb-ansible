# This Makefile helps to build and publish the Ansible collection on the Galaxy platform
#
# Build the collection:
#  make EDB_ANSIBLE_VERSION=x.y.z build
#
# Publish the collection once it has been built:
#  make EDB_ANSIBLE_VERSION=x.y.z API_KEY=xxxxxxxx publish
# Note: the API key can be found at https://galaxy.ansible.com/me/preferences
#
# Clean up the generated files:
#  make EDB_ANSIBLE_VERSION=x.y.z clean

EDB_ANSIBLE_VERSION ?= 3.0.0

DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

build:
	sed -E 's/version:.*/version: "$(EDB_ANSIBLE_VERSION)"/g' $(DIR)/galaxy.template.yml > $(DIR)/galaxy.yml
	ansible-galaxy collection build $(DIR)

publish:
	ansible-galaxy collection publish --api-key $(API_KEY) $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz

clean:
	rm -f $(DIR)/galaxy.yml
	rm -f $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz
