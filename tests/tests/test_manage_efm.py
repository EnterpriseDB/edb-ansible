import pytest
import json

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_type,
    get_primary,
    get_standbys,
    get_pg_unix_socket_dir,
    get_pg_version,
    get_pg_cluster_nodes
)

def test_manage_efm_pg_version():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    pg_version = get_pg_version()

    with host.sudo(pg_user):
        cmd = host.run('/usr/edb/efm-4.5/bin/efm_db_functions readpgversion main')
        result = cmd.stdout.strip()

    assert pg_version in result, \
        "efm service not correctly bound to postgres service"


def test_manage_efm_pg_replication_slots():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    standby_nodes = [node for node in get_standbys()]

    with host.sudo(pg_user):
        query = "Select slot_name from pg_replication_slots where active = 't'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))

        result = cmd.stdout.strip().split('\n')

    assert len(result) == len(standby_nodes), \
        "Standby nodes not configured correctly"