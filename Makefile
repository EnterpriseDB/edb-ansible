DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DIST := $(DIR)/dist
VERSION ?= $(shell cat $(DIR)/VERSION | head -n 1)

build:
	sed -E 's/version:.*/version: "$(VERSION)"/g' $(DIR)/galaxy.template.yml > $(DIR)/galaxy.yml
	ansible-galaxy collection build --output-path $(DIST) $(DIR)

publish:
	ansible-galaxy collection publish --api-key $(API_KEY) $(DIST)/hypersql_devops-postgres-$(VERSION).tar.gz

clean:
	rm -f $(DIR)/galaxy.yml
	rm -f $(DIST)/hypersql_devops-postgres-$(VERSION).tar.gz 

