import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pgbackrestserver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)


def test_setup_pgbackrestserver_packages():
    host = get_pgbackrestserver()
    packages = ['pgbackrest']

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages


def test_setup_pgbackrestserver_config_file():
    host = get_pgbackrestserver()
    ansible_vars = load_ansible_vars()
    config_file = ansible_vars['pgbackrest_configuration_file']

    assert host.file(config_file).exists, \
        "%s does not exist" % config_file


def test_setup_pgbackrestserver_sudo():
    host = get_pgbackrestserver()
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']

    with host.sudo(pgbackrest_user):
        cmd = host.run('pgbackrest -h')
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "%s could not be used as a sudo user" % pgbackrest_user