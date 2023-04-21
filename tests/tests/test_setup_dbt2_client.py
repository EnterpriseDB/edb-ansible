import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_dbt2_client,
    get_pg_version,
    get_primary,
    get_pg_unix_socket_dir
)

def test_setup_dbt2_client_packages():
    host = get_dbt2_client()[0]
    packages = [
        'dbt2-common'
    ]

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_dbt2_client_sudo():
    host = get_dbt2_client()[0]
    ansible_vars = load_ansible_vars()
    pg_owner = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_owner = 'enterprisedb'

    limit_file_path = ansible_vars['limit_file_path']

    cmd = host.run('cat %s | grep %s' % (limit_file_path, pg_owner))
    results = cmd.stdout.strip().split('\n')
    
    for result in results:
        assert '10000' in result, \
            "%s no file limits was not increased" % limit_file_path
