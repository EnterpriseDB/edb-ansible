import pytest

from conftest import (
    get_hosts,
    get_primary,
    get_standbys,
    get_pg_unix_socket_dir,
    get_enable_edb_tde
)


def test_setup_replication_user():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'repuser' and userepl = 't'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "repuser was not succesfully created"


def test_setup_replication_slots():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) > 0, \
        "Replication did not create replication slots"


def test_setup_replication_stat_replication():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    host = get_primary()
    rep_count = len(get_standbys())
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select application_name from pg_stat_replication"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) == rep_count, \
        "Replication was not successful on master"


def test_setup_replication_stat_wal_receiver():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    hosts = get_standbys()
    socket_dir = get_pg_unix_socket_dir()
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select slot_name from pg_stat_wal_receiver"
            cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
            result = cmd.stdout.strip().split('\n')

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), \
        "Replication was not successful on standby(s)"


def test_setup_replication_tde_enabled():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    hosts = get_standbys()
    socket_dir = get_pg_unix_socket_dir()
    res = []

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select data_encryption_version from pg_control_init where data_encryption_version = 1"
            cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
            result = cmd.stdout.strip().split('\n')

        if len(result) > 0:
            res.append(result)

    assert len(res) == len(hosts), \
        "TDE is not enabled on standby(s)"
