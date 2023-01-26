import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)

def test_setup_dbt7_packages():
    host = get_primary()
    packages = ['dbt7']

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_dbt7_user():
    ansible_vars = load_ansible_vars()
    pg_user = 'postgres'
    pg_group = 'postgres'
    pg_port = '5432'


    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_port = '5444'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    with host.sudo(pg_user):
        query = "Select * from pg_user WHERE usename='%s'" % pg_user
        cmd = host.run('psql -p %s -At -h %s -c "%s" postgres' % (pg_port, socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "%s was not sucessfully created." % pg_user
