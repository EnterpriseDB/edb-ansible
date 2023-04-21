import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_dbt2_driver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)

def test_setup_dbt2_driver_packages():
    host = get_dbt2_driver()[0]
    packages = [
        'dbttools',
        'dbt2-common'
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_dbt2_driver_sudo():
    host = get_dbt2_driver()[0]
    ansible_vars = load_ansible_vars()
    pg_user = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'

    with host.sudo(pg_user):
        cmd = host.run('env | grep USER')
        result = cmd.stdout.strip()
   
    assert pg_user in result, \
        "%s could not be used as a sudo user" % pg_user