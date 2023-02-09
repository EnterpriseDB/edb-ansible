import pytest
from conftest import get_os, get_pg_type, get_pg_version, get_primary, os_family


def test_install_dbserver_pg_centos():
    if os_family() != "RedHat":
        pytest.skip()
    if get_pg_type() != "PG":
        pytest.skip()

    host = get_primary()
    pg_version = get_pg_version()
    packages = [
        "glibc-common",
        "ca-certificates",
        "postgresql%s-libs" % pg_version,
        "postgresql%s" % pg_version,
        "postgresql%s-server" % pg_version,
        "postgresql%s-contrib" % pg_version,
        "sslutils_%s" % pg_version,
    ]
    if get_os() == "centos7":
        packages += [
            "python-pycurl",
            "libselinux-python",
            "python2-psycopg2",
            "python-ipaddress",
        ]
    elif get_os() == "rocky8":
        packages += ["python3-pycurl", "python3-libselinux", "python3-psycopg2"]
    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages

def test_install_dbserver_pg_debian():
    if os_family() != "Debian":
        pytest.skip()
    if get_pg_type() != "PG":
        pytest.skip()

    host = get_primary()
    pg_version = get_pg_version()
    packages = [
        "ca-certificates",
        "python3-pycurl",
        "python3-psycopg2",
        "postgresql-%s" % pg_version,
        "postgresql-server-dev-%s" % pg_version,
    ]
    if get_os() in ["debian9", "debian10"]:
        packages += ["python-psycopg2", "python-ipaddress"]
    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages
