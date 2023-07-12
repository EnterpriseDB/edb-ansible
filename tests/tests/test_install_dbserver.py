import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_version,
    get_pg_type,
    get_primary,
    os_family,
)


def test_install_dbserver_pg_centos():
    if os_family() != 'RedHat':
        pytest.skip()
    if get_pg_type() != 'PG':
        pytest.skip()

    host = get_primary()
    pg_version = get_pg_version()
    packages = [
        'glibc-common',
        'ca-certificates',
        'postgresql%s' % pg_version,
        'postgresql%s-server' % pg_version,
        'postgresql%s-contrib' % pg_version,
        'sslutils_%s' % pg_version,
    ]
    if get_os() == 'centos7':
        packages += [
            'python-pycurl',
            'libselinux-python',
            'python2-psycopg2',
            'python-ipaddress'
        ]
    elif get_os() in ['rocky8', 'almalinux8']:
        packages += [
            'python3-pycurl',
            'python3-libselinux',
            'python3-psycopg2'
        ]
    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages


def test_install_dbserver_epas_centos():
    if os_family() != 'RedHat':
        pytest.skip()
    if get_pg_type() != 'EPAS':
        pytest.skip()

    host = get_primary()
    pg_version = int(get_pg_version())
    packages = [
        'edb-as%s-server' % pg_version,
        'edb-as%s-server-core' % pg_version,
        'edb-as%s-server-contrib' % pg_version,
        'edb-as%s-server-libs' % pg_version,
        'edb-as%s-server-client' % pg_version,
        'edb-as%s-server-sslutils' % pg_version,
        'edb-as%s-server-indexadvisor' % pg_version,
        'edb-as%s-server-sqlprofiler' % pg_version,
        'edb-as%s-server-sqlprotect' % pg_version,
        'edb-as%s-server-sslutils' % pg_version,
        'edb-as%s-server-edb_wait_states' % pg_version,
    ]
    if get_os() in ['centos7', 'oraclelinux7']:
        packages += [
            'python2-pip',
            'python2-psycopg2',
            'python-ipaddress',
        ]
    elif get_os() in ['rocky8', 'almalinux8']:
        packages += [
            'python3-pip',
            'python3-psycopg2',
        ]
    if pg_version > 10:
        packages += [
            'edb-as%s-server-llvmjit' % pg_version,
        ]
    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages


def test_install_dbserver_pg_debian():
    if os_family() != 'Debian':
        pytest.skip()
    if get_pg_type() != 'PG':
        pytest.skip()

    host = get_primary()
    pg_version = get_pg_version()
    packages = [
        'ca-certificates',
        'python3-pycurl',
        'python3-psycopg2',
        'postgresql-%s' % pg_version,
        'postgresql-server-dev-%s' % pg_version,
        'postgresql-%s-sslutils' % pg_version,
    ]
    if get_os() in ['debian9', 'debian10']:
        packages += [
            'python-psycopg2',
            'python-ipaddress'
        ]
    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages


def test_install_dbserver_epas_debian():
    if os_family() != 'Debian':
        pytest.skip()
    if get_pg_type() != 'EPAS':
        pytest.skip()

    host = get_primary()
    pg_version = int(get_pg_version())
    packages = [
        'python3-pip',
        'python3-psycopg2',
        'edb-as%s-server' % pg_version,
        'edb-as%s-server-core' % pg_version,
        'edb-as%s-server-client' % pg_version,
        'edb-as%s-server-sslutils' % pg_version,
        'edb-as%s-server-indexadvisor' % pg_version,
        'edb-as%s-server-sqlprofiler' % pg_version,
        'edb-as%s-server-sqlprotect' % pg_version,
        'edb-as%s-server-sslutils' % pg_version,
    ]
    if get_os() in ['debian9', 'debian10']:
        packages += [
            'python-psycopg2',
            'python-ipaddress',
        ]
    if pg_version < 14:
        packages += [
            'edb-as%s-server-edb-modules' % pg_version,
        ]
    else:
        packages += [
            'edb-as%s-server-edb-wait-states' % pg_version,
        ]
    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages
