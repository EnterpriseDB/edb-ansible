import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_version,
    get_pg_type,
    get_pg_unix_socket_dir,
    get_primary,
    os_family,
    get_enable_edb_tde
)


def test_init_dbserver_files():
    if not get_enable_edb_tde():
        pytest.skip()

    ansible_vars = load_ansible_vars()

    pg_data = ansible_vars['pg_data']
    pg_wal = ansible_vars['pg_wal']

    pg_user = 'enterprisedb'
    pg_group = 'enterprisedb'

    host = get_primary()

    for pg_dir in [pg_data, pg_wal]:
        assert host.file(pg_dir).exists, \
            "%s does not exist" % pg_dir

        assert host.file(pg_dir).is_directory, \
            "%s is not a directory" % pg_dir

        assert host.file(pg_dir).user == pg_user, \
            "%s is not owned by postgres" % pg_dir

        assert host.file(pg_dir).group == pg_group, \
            "%s group is not postgres" % pg_dir

    # Test PGWAL
    assert host.file("%s/pg_wal" % pg_data).exists, \
        "%s/pg_wal does not exist" % pg_data
    assert host.file("%s/pg_wal" % pg_data).is_symlink, \
        "%s/pg_wal is not a symlink" % pg_data
    assert host.file("%s/pg_wal" % pg_data).linked_to == pg_wal, \
        "%s/pg_wal is not linked to %s" % (pg_data, pg_wal)


def test_init_dbserver_service():
    if not get_enable_edb_tde():
        pytest.skip()

    host = get_primary()
    pg_version = get_pg_version()

    if os_family() == 'RedHat':
        if get_pg_type() == 'PG':
            service = 'postgresql-%s' % pg_version
        elif get_pg_type() == 'EPAS':
            service = 'edb-as-%s' % pg_version
    elif os_family() == 'Debian':
        if get_pg_type() == 'PG':
            service = 'postgresql@%s-main' % pg_version
        elif get_pg_type() == 'EPAS':
            service = 'edb-as@%s-main' % pg_version

    assert host.service(service).is_running, \
        "Postgres service not running"

    assert host.service(service).is_enabled, \
        "Postgres service not enabled"


def test_init_dbserver_socket():
    if not get_enable_edb_tde():
        pytest.skip()

    host = get_primary()

    sockets = [
            "tcp://5444",
    ]
    if os_family() == 'RedHat':
        sockets.append(
            "unix:///var/run/edb/as%s/.s.PGSQL.5444" % get_pg_version()
        )
    elif os_family() == 'Debian':
        sockets.append(
            "unix:///var/run/edb-as/.s.PGSQL.5444"
        )
    for socket in sockets:
        assert host.socket(socket).is_listening, \
            "Postgres is not listening on %s" % socket


def test_init_dbserver_data_directory():
    if not get_enable_edb_tde():
        pytest.skip()

    ansible_vars = load_ansible_vars()
    pg_data = ansible_vars['pg_data']

    pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "SELECT setting FROM pg_settings WHERE name = 'data_directory'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))

        data_directory = cmd.stdout.strip()
        assert host.file(data_directory).linked_to == pg_data, \
            "Postgres data_directory is not linked to '%s'" % pg_data


def test_setup_replication_tde_enabled():
    if not get_enable_edb_tde():
        pytest.skip()

    pg_user = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    res = []

    with host.sudo(pg_user):
        query = "Select data_encryption_version from pg_control_init where data_encryption_version = 1"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip().split('\n')

    if len(result) > 0:
        res.append(result)

    assert len(res) == 1, \
        "TDE is not enabled on Primary"
