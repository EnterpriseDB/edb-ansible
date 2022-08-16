import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_barmanserver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)

def test_setup_barmanserver_packages():
    host = get_barmanserver()
    packages = [
        'barman',
        'barman-cli'
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_barmanserver_config_file():
    host = get_barmanserver()
    ansible_vars = load_ansible_vars()
    config_file = ansible_vars['barman_configuration_file']

    assert host.file(config_file).exists, \
        "%s does not exist" % config_file

def test_setup_barmanserver_sudo():
    host = get_barmanserver()
    ansible_vars = load_ansible_vars()
    barman_user = ansible_vars['barman_user']

    with host.sudo(barman_user):
        cmd = host.run('barman -h')
        result = cmd.stdout.strip()
    
    assert len(result) > 0, \
        "%s could not be used as a sudo user" % barman_user