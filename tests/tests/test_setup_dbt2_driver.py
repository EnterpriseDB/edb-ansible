import pytest

from conftest import (
    get_pg_type,
    get_dbt2_driver,
)


def test_setup_dbt2_driver_packages():
    host = get_dbt2_driver()[0]
    packages = [
        'perf',
        'rsync',
        'tmux',
        'fuse',
        'fuse-libs',
        'sysstat',
        'fontconfig',
        'dejavu-fonts-common'
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % package


def test_setup_dbt2_driver_appimage():
    host = get_dbt2_driver()[0]
    appimage_location = "/usr/bin/dbt2"

    assert host.file(appimage_location).exists, \
        "DBT-2 AppImage not installed correctly on driver."


def test_setup_dbt2_driver_sudo():
    host = get_dbt2_driver()[0]
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    with host.sudo(pg_user):
        cmd = host.run('env | grep USER')
        result = cmd.stdout.strip()
   
    assert pg_user in result, \
        "%s could not be used as a sudo user" % pg_user
