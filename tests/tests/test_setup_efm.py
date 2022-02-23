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
    get_pg_cluster_nodes
)

def test_setup_efm_user():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host= get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'efm' and userepl = 't'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "efm user was not succesfully created"

def test_setup_efm_service():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host= get_primary()
    nodes = [node for node in get_pg_cluster_nodes()]
    
    with host.sudo(pg_user):
        cmd = host.run('/usr/edb/efm-4.4/bin/efm cluster-status main | grep UP')
        result = cmd.stdout.strip().split('\n')

    assert len(result) == len(nodes), \
        "EFM service has not started on all the nodes"

def test_setup_efm_pg_read_all_settings():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host= get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = r"\du"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().replace('\nProfile', "").split('\n')
        efm_index = [idx for idx, role in enumerate(result) if 'efm' in role][0]

    assert 'pg_read_all_settings' in result[efm_index], \
        "EFM role is not a pg_read_all_settings"