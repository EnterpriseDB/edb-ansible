# This Makefile helps to build, install or publish the Ansible
# collection on the Galaxy platform.
# Target version can be passed with the EDB_ANSIBLE_VERSION env.
# variable. The default version is taken from the VERSION file
# content.
#
# Build the collection:
#  make build
#
# Publish the collection once it has been built:
#  make API_KEY=xxxxxxxx publish
# Note: the API key can be found at https://galaxy.ansible.com/me/preferences
#
# Clean up the generated files:
#  make clean
#
# Clean up, build and install the collection:
#  make install

DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
EDB_ANSIBLE_VERSION ?= $(shell cat $(DIR)/VERSION | head -n 1)

build:
	sed -E 's/version:.*/version: "$(EDB_ANSIBLE_VERSION)"/g' $(DIR)/galaxy.template.yml > $(DIR)/galaxy.yml
	ansible-galaxy collection build $(DIR)

publish:
	ansible-galaxy collection publish --api-key $(API_KEY) $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz

clean:
	rm -f $(DIR)/galaxy.yml
	rm -f $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz

install: clean build
	ansible-galaxy collection install $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz --force

install-build:
	ansible-galaxy collection install $(DIR)/edb_devops-edb_postgres-$(EDB_ANSIBLE_VERSION).tar.gz --force
