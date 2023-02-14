DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DIST := $(DIR)/dist
DIST_FOR_TEST := $(DIR)/tests/docker
VERSION ?= $(shell cat $(DIR)/VERSION | head -n 1)

build:
	sed -E 's/version:.*/version: "$(VERSION)"/g' $(DIR)/galaxy.template.yml > $(DIR)/galaxy.yml
	ansible-galaxy collection build --output-path $(DIST) $(DIR)

build_for_test:
	sed -E 's/version:.*/version: "$(VERSION)"/g' $(DIR)/galaxy.template.yml > $(DIR)/galaxy.yml
	ansible-galaxy collection build --output-path $(DIST_FOR_TEST) $(DIR)

publish:
	ansible-galaxy collection publish --api-key $(API_KEY) $(DIST)/tmax_opensql-postgres-$(VERSION).tar.gz

clean:
	rm -f $(DIR)/galaxy.yml
	rm -f $(DIST)/tmax_opensql-postgres-$(VERSION).tar.gz 

clean_for_test:
	rm -f $(DIR)/galaxy.yml
	rm -f $(DIST_FOR_TEST)/tmax_opensql-postgres-$(VERSION).tar.gz