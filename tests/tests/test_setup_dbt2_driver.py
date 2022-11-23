import pytest
from conftest import (
    get_dbt2_driver,
    get_pg_type,
    get_pg_unix_socket_dir,
    get_pg_version,
    get_primary,
    load_ansible_vars,
)


def test_setup_dbt2_driver_packages():
    host = get_dbt2_driver()[0]
    packages = ["dbt2-driver", "dbt2-exec", "dbt2-scripts"]

    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages


def test_setup_dbt2_driver_sudo():
    host = get_dbt2_driver()[0]
    ansible_vars = load_ansible_vars()
    postgres_user = ansible_vars["postgres_user"]

    with host.sudo(postgres_user):
        cmd = host.run("env | grep USER")
        result = cmd.stdout.strip()

    assert postgres_user in result, (
        "%s could not be used as a sudo user" % postgres_user
    )
