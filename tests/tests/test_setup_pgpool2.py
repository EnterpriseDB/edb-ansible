import pytest
from conftest import get_pg_type, get_pgpool2, get_primary, load_ansible_vars


def test_setup_pgpool2_EPAS():
    if get_pg_type() != "EPAS":
        pytest.skip()
    host = get_pgpool2()[0]
    service = "edb-pgpool-4.3"

    assert host.service(service).is_running, "pgpool2 service not running"

    assert host.service(service).is_enabled, "pgpool2 service not enabled"


def test_setup_pgpool2_PG():
    if get_pg_type() != "PG":
        pytest.skip()
    host = get_pgpool2()[0]
    service = "pgpool-II"

    assert host.service(service).is_running, "pgpool2 service not running"

    assert host.service(service).is_enabled, "pgpool2 service not enabled"


def test_setup_pgpool_PG_packages():
    if get_pg_type() != "PG":
        pytest.skip()
    host = get_pgpool2()[0]
    packages = ["pgpool-II", "openssl"]

    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages


def test_setup_pgpool_EPAS_packages():
    if get_pg_type() != "EPAS":
        pytest.skip()
    host = get_pgpool2()[0]
    packages = ["edb-pgpool43", "openssl"]

    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages


def test_setup_pgpool_test_user():
    ansible_vars = load_ansible_vars()
    pgpool2_user = ansible_vars["pgpool2_users"][0]["name"]
    pgpool2_password = ansible_vars["pgpool2_users"][0]["pass"]
    pgpool2_port = ansible_vars["pgpool2_port"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgpool2_address = get_pgpool2()[0]
    address = str(pgpool2_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = '%s'" % pgpool2_user
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" postgres'
            % (pgpool2_password, pgpool2_user, address, pgpool2_port, query)
        )
        result = cmd.stdout.strip()

    assert len(result) > 0, "pgpool test user was not created sucessfully."


def test_setup_pgpool_users():
    ansible_vars = load_ansible_vars()
    pgpool2_user = ansible_vars["pgpool2_users"][0]["name"]
    pgpool2_password = ansible_vars["pgpool2_users"][0]["pass"]
    pgpool2_port = ansible_vars["pgpool2_port"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgpool2_address = get_pgpool2()[0]
    address = str(pgpool2_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "Select usename from pg_user where usename = '%s' or usename ='%s'" % (
            "pgpool",
            "pgpool2",
        )
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" postgres'
            % (pgpool2_password, pgpool2_user, address, pgpool2_port, query)
        )
        result = cmd.stdout.strip().split("\n")

    assert len(result) == 2, "pgpool users was not created sucessfully."


def test_setup_pgpool_loadbalance():
    ansible_vars = load_ansible_vars()
    pgpool2_user = ansible_vars["pgpool2_users"][0]["name"]
    pgpool2_password = ansible_vars["pgpool2_users"][0]["pass"]
    pgpool2_port = ansible_vars["pgpool2_port"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgpool2_address = get_pgpool2()[0]
    address = str(pgpool2_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "PGPOOL SHOW load_balance_mode;"
        cmd = host.run(
            "PGPASSWORD=%s psql -At -U %s -h %s -p %s -c '%s' postgres"
            % (pgpool2_password, pgpool2_user, address, pgpool2_port, query)
        )
        result = cmd.stdout.strip()

    assert result == "on", "Load Balance is not enabled."
