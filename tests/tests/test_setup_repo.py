import pytest
from conftest import EDB_ENABLE_REPO, get_pg_type, get_primary, os_family


def test_setup_repo_edb_centos():
    if not EDB_ENABLE_REPO:
        pytest.skip()

    if os_family() != "RedHat":
        pytest.skip()

    host = get_primary()
    cmd = host.run("yum repolist")
    assert cmd.succeeded, "Unable to list the package repository list"
    assert (
        "EnterpriseDB RPMs" in cmd.stdout
    ), "Access to the EDB package repository not configured"


def test_setup_repo_pgdg_centos():
    if os_family() != "RedHat":
        pytest.skip()

    if get_pg_type() != "PG":
        pytest.skip()

    host = get_primary()
    cmd = host.run("yum repolist")
    assert cmd.succeeded, "Unable to list the package repository list on %s" % host
    assert (
        "PostgreSQL common RPMs for RHEL" in cmd.stdout
    ), "Access to the PGDG package repository not configured"


def test_setup_repo_edb_debian():
    if not EDB_ENABLE_REPO:
        pytest.skip()

    if os_family() != "Debian":
        pytest.skip()

    host = get_primary()
    cmd = host.run("grep -rhE ^deb /etc/apt/sources.list*")
    assert cmd.succeeded, "Unable to list the package repository list"
    assert (
        "apt.enterprisedb.com" in cmd.stdout
    ), "Access to the EDB package repository not configured"


def test_setup_repo_pgdg_debian():
    if os_family() != "Debian":
        pytest.skip()

    if get_pg_type() != "PG":
        pytest.skip()

    host = get_primary()
    cmd = host.run("grep -rhE ^deb /etc/apt/sources.list*")
    assert cmd.succeeded, "Unable to list the package repository list"
    assert (
        "apt.postgresql.org" in cmd.stdout
    ), "Access to the PGDG package repository not configured"
