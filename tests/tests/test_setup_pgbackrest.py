import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pgbackrestserver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)


def test_setup_pgbackrest_config():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        cmd = host.run('pgbackrest --stanza=main check')
        result = cmd.stdout.strip()

    assert 'completed successfully' in result, \
        "Configuration for pgBackRest is not properly done."

def test_setup_pgbackrest_backup():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        cmd = host.run('pgbackrest --stanza=main info')
        result = cmd.stdout.strip()

    assert 'full backup' in result, \
        "Backup for PgBackrest main cluster has failed"

def test_setup_pgbackrest_repo():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        cmd = host.run('pgbackrest repo-ls')
        result = cmd.stdout.strip()

    assert 'archive' in result, \
        "Archive repo for PgBackRest server has not been configured properly"

