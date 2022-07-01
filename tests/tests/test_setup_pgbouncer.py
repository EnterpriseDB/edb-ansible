import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pgbouncer,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir,
    get_os
)

def test_setup_pgbouncer_service():
    host = get_pgbouncer()[0]
    service = 'pgbouncer'

    if get_pg_type() == 'EPAS':
        if get_os() == 'debian10':
            service = 'edb-pgbouncer116'
        elif get_os().startswith(("centos", "rocky")):
            service = 'edb-pgbouncer-1.16'

    assert host.service(service).is_running, \
        "pgbouncer service not running"

    assert host.service(service).is_enabled, \
        "pgbouncer service not enabled"

def test_setup_pgbouncer_packages():
    host = get_pgbouncer()[0]

    packages = [
        'pgbouncer'
    ]

    if get_pg_type() == 'EPAS':
        packages = [
            'edb-pgbouncer116'
        ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_pgbouncer_test_user():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars['pgbouncer_auth_user_list'][0]['username']
    pgbouncer_password = ansible_vars['pgbouncer_auth_user_list'][0]['password']
    pgbouncer_port = ansible_vars['pgbouncer_listen_port']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    pgbouncer_address= get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split('//')[1]
    host = get_primary()
    
    with host.sudo(pg_user):
        query = "SHOW users"
        cmd = host.run('PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s' % (pgbouncer_password, 
                                                                                                pgbouncer_user, 
                                                                                                address, 
                                                                                                pgbouncer_port, 
                                                                                                query,
                                                                                                pgbouncer_user))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pgbouncer test user was not created sucessfully."

def test_setup_pgbouncer_config():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars['pgbouncer_auth_user_list'][0]['username']
    pgbouncer_password = ansible_vars['pgbouncer_auth_user_list'][0]['password']
    pgbouncer_port = ansible_vars['pgbouncer_listen_port']
    pgbouncer_admin_user = ansible_vars['pgbouncer_admin_users']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    pgbouncer_address= get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split('//')[1]
    host = get_primary()
    
    with host.sudo(pg_user):
        query = "SHOW config"
        cmd = host.run('PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s' % (pgbouncer_password, 
                                                                                                pgbouncer_user, 
                                                                                                address, 
                                                                                                pgbouncer_port, 
                                                                                                query,
                                                                                                'admin_users'))
        result = cmd.stdout.strip()

    assert pgbouncer_admin_user in result, \
        "pgbouncer admin user was not configured properly."

def test_setup_pgbouncer_port():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars['pgbouncer_auth_user_list'][0]['username']
    pgbouncer_password = ansible_vars['pgbouncer_auth_user_list'][0]['password']
    pgbouncer_port = ansible_vars['pgbouncer_listen_port']
    pgbouncer_admin_user = ansible_vars['pgbouncer_admin_users']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    pgbouncer_address= get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split('//')[1]
    host = get_primary()
    
    with host.sudo(pg_user):
        query = "SHOW active_sockets"
        cmd = host.run('PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s' % (pgbouncer_password, 
                                                                                                pgbouncer_user, 
                                                                                                address, 
                                                                                                pgbouncer_port, 
                                                                                                query,
                                                                                                pgbouncer_port))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pgbouncer port was not configured properly."

