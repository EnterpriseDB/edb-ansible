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


def test_setup_hammerdb_load_tproc_c():
    ansible_vars = load_ansible_vars()
    load_tproc_c = ansible_vars["load-tproc-c"]
    host = get_hammerdb()[0]

    assert host.file(load_tproc_c).exists, "Load-TProc-C wasn't sucessfully installed"


def test_setup_hammerdb_run_tproc_c():
    ansible_vars = load_ansible_vars()
    run_tproc_c = ansible_vars["run-tproc-c"]
    host = get_hammerdb()[0]

    assert host.file(run_tproc_c).exists, "Run-TProc-C wasn't sucessfully installed"


def test_setup_hammerdb_max_connections():
    ansible_vars = load_ansible_vars()
    pg_user = "postgres"
    pg_group = "postgres"
    max_connections = ansible_vars["max_connections"]

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"
        pg_group = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    with host.sudo(pg_user):
        query = "Show max_connections"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert (
        result == max_connections
    ), "Max connections was not significantly configured."


def test_setup_hammerdb_max_wal_size():
    ansible_vars = load_ansible_vars()
    pg_user = "postgres"
    pg_group = "postgres"
    max_wal_size = ansible_vars["max_wal_size"]

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"
        pg_group = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    with host.sudo(pg_user):
        query = "Show max_wal_size"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert result == max_wal_size, "Max wal size was not significantly configured."
