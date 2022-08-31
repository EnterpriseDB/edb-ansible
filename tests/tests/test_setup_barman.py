import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_barmanserver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)

def test_setup_barman_backup():
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    host = get_barmanserver()

    with host.sudo(barman_user):
        cmd = host.run('barman list-server')
        result = cmd.stdout.strip()

    assert "primary1" in result, \
        "%s backup server was not configured correctly" % "primary1"

def test_setup_barman_home_dir():
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    barman_home = ansible_vars['barman_home']
    host = get_barmanserver()

    with host.sudo(barman_user):
        cmd = host.run('barman show-server primary1-main | grep barman_home')
        result = cmd.stdout.strip()

    assert barman_home in result, \
        "%s directory was not configured correctly" % barman_home

def test_setup_barman_status():
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    barman_home = ansible_vars['barman_home']
    host = get_barmanserver()

    with host.sudo(barman_user):
        cmd = host.run('barman status primary1-main | grep Active')
        result = cmd.stdout.strip()

    assert "True" in result, \
        "primary1-main's server status is not active"

def test_setup_barman_user():
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    port = '5432'
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        port = '5444'

    host= get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = '%s'" % barman_user
        cmd = host.run('psql -At -p %s -h %s -c "%s" postgres' % (port, socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "Barman user does not exist in primary database"

def test_setup_barman_logical_wal_level():
    # Make sure setup_barman does not override wal_level if it has been
    # previously configured to 'logical'.
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    port = '5432'
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        port = '5444'

    host= get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "SELECT setting FROM pg_settings WHERE name = 'wal_level'"
        cmd = host.run(
            'psql -At -p %s -h %s -c "%s" postgres' % (port, socket_dir, query)
        )
        result = cmd.stdout.strip()

    assert result == 'logical', \
        "wal_level should be set to 'logical'"

def test_setup_barman_backup():
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']
    barman_home = ansible_vars['barman_home']
    host = get_barmanserver()

    with host.sudo(barman_user):
        cmd = host.run('barman backup primary1-main | grep completed')
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "Backup for primary1-main's server has failed"
