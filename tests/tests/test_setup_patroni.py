import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_type,
    get_primary,
    get_standbys,
    get_pg_unix_socket_dir,
    get_pg_bin_dir
)


def test_setup_patroni_user():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    pg_bin_dir = get_pg_bin_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'repuser' and userepl = 't'"
        cmd = host.run('%s/psql -At -h %s -c "%s" postgres' % (pg_bin_dir, socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "repuser was not succesfully created"


def test_setup_patroni_slots():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    pg_bin_dir = get_pg_bin_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots"
        cmd = host.run('%s/psql -At -h %s -c "%s" postgres' % (pg_bin_dir, socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) > 0, \
        "Replication did not create replication slots"


def test_setup_patroni_stat_replication():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    host = get_primary()
    rep_count = len(get_standbys())
    socket_dir = get_pg_unix_socket_dir()
    pg_bin_dir = get_pg_bin_dir()
    
    with host.sudo(pg_user):
        query = 'Select application_name from pg_stat_replication'
        cmd = host.run("%s/psql -At -h %s -c '%s' postgres" % (pg_bin_dir, socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) == rep_count, \
        "Replication was not successful on master"


def test_setup_patroni_stat_wal_receiver():
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    hosts = get_standbys()
    socket_dir = get_pg_unix_socket_dir()
    pg_bin_dir = get_pg_bin_dir()
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select slot_name from pg_stat_wal_receiver"
            cmd = host.run('%s/psql -At -h %s -c "%s" postgres' % (pg_bin_dir, socket_dir, query))
            result = cmd.stdout.strip().split('\n')

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), \
        "Replication was not successful on standby(s)"
