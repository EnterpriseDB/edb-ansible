import os

import pytest
from conftest import (
    get_hammerdb,
    get_hosts,
    get_os,
    get_pg_type,
    get_pg_unix_socket_dir,
    get_pg_version,
    get_primary,
    load_ansible_vars,
)


def test_setup_hammerdbserver_dir():
    ansible_vars = load_ansible_vars()
    pg_data = ansible_vars["pg_data"]
    hammerdb = ansible_vars["hammerdb"]
    host = get_hammerdb()[0]

    assert host.file(hammerdb).exists, "HammerDB wasn't sucessfully installed"


def test_setup_hammerdbserver_install_file():
    ansible_vars = load_ansible_vars()
    pg_data = ansible_vars["pg_data"]
    hammerdb_version = ansible_vars["hammerdb_version"]
    host = get_hammerdb()[0]

    assert host.file(
        "HammerDB-%s-Linux.tar.gz" % hammerdb_version
    ).exists, "HammerDB install file wasn't downloaded"
