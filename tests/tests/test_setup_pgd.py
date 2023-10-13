import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_pg_type,
    get_primary,
    get_pg_unix_socket_dir
)


def test_setup_pgd_user():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'pgd_replication_user' and userepl = 't'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pgd_replication_user was not succesfully created"


def test_setup_pgd_slots():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) > 0, \
        "Replication did not create replication slots"


def test_setup_pgd_stat_replication():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    rep_count = len(get_hosts('primary'))-1
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select application_name from pg_stat_replication"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) == rep_count, \
        "Replication was not successful on master"


def test_setup_pgd_stat_wal_receiver():
    ansible_vars = load_ansible_vars()
    pgd_repuser = ansible_vars['pgd_replication_user']
    pgd_repuser_pwd = ansible_vars['pgd_replication_user_password']

    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    lead_master = get_primary()
    primary_hosts = get_hosts('primary')
    hosts = []
    for item in primary_hosts:
        if item != lead_master:
            hosts.append(item)

    socket_dir = get_pg_unix_socket_dir()
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select slot_name from pg_stat_wal_receiver"
            cmd = host.run('PGPASSWORD=%s psql -At -h %s -U %s -c "%s" postgres'
                           % (pgd_repuser_pwd, socket_dir, pgd_repuser, query))
            result = cmd.stdout.strip().split('\n')

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), \
        "Replication was not successful on standby(s)"


def test_setup_local_node_created():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    socket_dir = get_pg_unix_socket_dir()
    hosts = get_hosts('primary')
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "SELECT node_name FROM bdr.local_node_info "
            cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
            result = cmd.stdout.strip().split('\n')

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), \
        "PGD local node wasn't created correctly"
