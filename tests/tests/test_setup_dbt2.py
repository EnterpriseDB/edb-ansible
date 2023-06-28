import pytest

from conftest import (
    get_pg_type,
    get_primary,
    get_pg_unix_socket_dir
)


def test_setup_dbt2_packages():
    host = get_primary()
    packages = [
        'perf',
        'rsync',
        'tmux',
        'fuse',
        'fuse-libs',
        'sysstat'
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages


def test_setup_dbt2_appimage():
    host = get_primary()
    appimage_location = "/usr/bin/dbt2"

    assert host.file(appimage_location).exists, \
        "DBT-2 AppImage not installed correctly on primary."


def test_setup_dbt2_user():
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
        "%s was not successfully created." % pg_user
