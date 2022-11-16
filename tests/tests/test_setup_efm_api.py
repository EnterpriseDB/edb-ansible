import pytest
import json

from conftest import (
    get_pg_cluster_nodes,
    get_os
)

def test_setup_efm_api_package():
    if get_os() in ['centos7', 'oraclelinux7', 'redhat7']:
        for (_, host) in get_pg_cluster_nodes():
            assert host.package("efm-api-node-state").is_installed, \
                "Package efm-api-node-state not installed"

def test_setup_efm_api_service():
    if get_os() in ['centos7', 'oraclelinux7', 'redhat7']:
        for (_, host) in get_pg_cluster_nodes():
            assert host.service("efm-api-node-state").is_running, \
                "efm-api-node-state service not running"
            assert host.service("efm-api-node-state").is_enabled, \
                "efm-api-node-state service not enabled"

def test_setup_efm_api_port():
    if get_os() in ['centos7', 'oraclelinux7', 'redhat7']:
        for (_, host) in get_pg_cluster_nodes():
            assert host.socket("tcp://0.0.0.0:8000").is_listening, \
                "efm-api-node is not listening on 0.0.0.0:8000"
