import pytest

from conftest import (
    get_pg_type,
    get_primary,
    get_pemserver,
    get_pg_version,
    get_pg_unix_socket_dir,
    get_pg_nodes
)

def test_setup_pemagent_pemagent():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host= get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'pemagent'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pemagent user was not succesfully created"

def test_setup_pemagent_agents():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host= get_pemserver()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select id from pem.agent"
        cmd = host.run('psql -At -h %s -c "%s" pem' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    # Seeing if number of agents is equal to the number of nodes: 3
    assert len(result) == 3, \
        "Pem agents were created sucessfuly."

def test_setup_pemagent_service():
    host= get_primary()
    pg_version = get_pg_version()
    service = 'pemagent'

    assert host.service(service).is_running, \
        "Pemagent service not running"

    assert host.service(service).is_enabled, \
        "Pemagent service not enabled"

def test_setup_pemagent_packages():
    host= get_pemserver()
    pg_version = get_pg_version()
    packages = [
        'edb-pem-agent',
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

