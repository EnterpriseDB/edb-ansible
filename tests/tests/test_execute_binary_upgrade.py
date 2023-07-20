import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    os_family,
    get_pg_type,
    get_primary,
    get_standbys,
)


def test_configuration_files():
    ansible_vars = load_ansible_vars()

    new_pg_version = ansible_vars['new_pg_version']

    if os_family() == 'RedHat':
        new_pg_config_file = '/var/lib/pgsql/%s/main/data/postgresql.conf' % new_pg_version
        if get_pg_type() == 'EPAS':
            new_pg_config_file = '/var/lib/edb/as%s/main/data/postgresql.conf' % new_pg_version
    elif os_family() == 'Debian':
        new_pg_config_file = '/etc/postgresql/%s/main/postgresql.conf' % new_pg_version
        if get_pg_type() == 'EPAS':
            new_pg_config_file = '/etc/edb-as/%s/main/postgresql.conf' % new_pg_version

    host = get_primary()

    assert host.file(new_pg_config_file).exists, \
        "New cluster configuration files were not properly created."


def test_new_pg_service():
    ansible_vars = load_ansible_vars()

    new_pg_version = ansible_vars['new_pg_version']

    if get_pg_type() == 'EPAS':
        if os_family() == 'RedHat':
            service = 'edb-as-%s' % new_pg_version
        elif os_family() == 'Debian':
            service = 'edb-as@%s-main' % new_pg_version
    elif get_pg_type() == 'PG':
        if os_family() == 'RedHat':
            service = 'postgresql-%s' % new_pg_version
        elif os_family() == 'Debian':
            service = 'postgresql@%s' % new_pg_version

    host = get_primary()

    assert host.service(service).is_running, \
        "new postgres service not running"


