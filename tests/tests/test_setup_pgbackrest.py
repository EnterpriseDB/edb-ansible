import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pgbackrestserver,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)


# def test_setup_pgbackrest_backup():
#     ansible_vars = load_ansible_vars()
#     pgbackrest_user = ansible_vars['pgbackrest_user']
#     host = get_pgbackrestserver()
#
#     with host.sudo(pgbackrest_user):
#         cmd = host.run('pgbackrest list-server')
#         result = cmd.stdout.strip()
#
#     assert "primary1" in result, \
#         "%s backup server was not configured correctly" % "primary1"


# def test_setup_pgbackrest_home_dir():
#     ansible_vars = load_ansible_vars()
#     pgbackrest_user = ansible_vars['pgbackrest_user']
#     pgbackrest_home = ansible_vars['pgbackrest_home']
#     host = get_pgbackrestserver()
#
#     with host.sudo(pgbackrest_user):
#         cmd = host.run('pgbackrest show-server primary1-main | grep pgbackrest_home')
#         result = cmd.stdout.strip()
#
#     assert pgbackrest_home in result, \
#         "%s directory was not configured correctly" % pgbackrest_home


def test_setup_pgbackrest_status():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    pgbackrest_home = ansible_vars['pgbackrest_home']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        cmd = host.run('pgbackrest status | grep Active')
        result = cmd.stdout.strip()

    assert "True" in result, \
        "primary1-main's server status is not active"

def test_setup_pgbackrest_config():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    pgbackrest_home = ansible_vars['pgbackrest_home']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        check_command = "pgbackrest --stanza=main check"
        cmd = host.run('pgbakrest --stanza=main check')
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "Configuration for pgBackRest is not properly done."

def test_setup_pgbackrest_backup():
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars['pgbackrest_user']
    pgbackrest_home = ansible_vars['pgbackrest_home']
    host = get_pgbackrestserver()

    with host.sudo(pgbackrest_user):
        # insert archive_command (setup_pgbackrest/main) here:
        # archive_command = "pgbackrest --stanza={{ pg_instance_name }} archive-push %p"
        cmd = host.run('pgbackrest --stanza=main archive-push %p | grep completed')
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "Backup for primary1-main's server has failed"

