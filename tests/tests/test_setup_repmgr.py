import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_os,
    get_standbys,
    get_pg_version,
    get_primary,
    get_witness,
    get_pg_unix_socket_dir,
    os_family,
)

def test_setup_repmgr_service_redhat():
    if get_os().startswith('debian') or get_os().startswith('ubuntu'):
        pytest.skip()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]
    pg_version = get_pg_version()
    service = 'repmgr-%s' % pg_version
    for host in hosts:
        assert host.service(service).is_running, \
            "Repmgr service not running"

def test_setup_repmgr_service_debian():
    if os_family() != 'Debian':
        pytest.skip()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]
    service = 'repmgrd'
    for host in hosts:
        assert host.service(service).is_running, \
            "Repmgr service not running"

def test_setup_repmgr_packages_redhat():
    if os_family() != 'RedHat':
        pytest.skip()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]
    pg_version = get_pg_version()
    packages = [
        'repmgr_%s' % pg_version
    ]
    for host in hosts:
        for package in packages:
            assert host.package(package).is_installed, \
                "Package %s not installed" % packages

def test_setup_repmgr_packages_debian():
    if os_family() != 'Debian':
        pytest.skip()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]
    pg_version = get_pg_version()
    packages = [
        'postgresql-%s-repmgr' % pg_version
    ]
    for host in hosts:
        for package in packages:
            assert host.package(package).is_installed, \
                "Package %s not installed" % packages

def test_setup_repmgr_user():
    pg_user = 'postgres'
    pg_group = 'postgres'

    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]
    socket_dir = get_pg_unix_socket_dir()

    for host in hosts:
        with host.sudo(pg_user):
            query = "Select * from pg_user where usename = 'repmgr'"
            cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
            result = cmd.stdout.strip()

        assert len(result) > 0, \
            "repmgr was not succesfully created"

def test_setup_repmgr_node_status_redhat():
    if os_family() != 'RedHat':
        pytest.skip()

    pg_user = 'postgres'
    pg_group = 'postgres'
    pg_version = get_pg_version()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]

    for host in hosts:
        with host.sudo(pg_user):
            cmd = host.run('/usr/pgsql-%s/bin/repmgr -f /etc/repmgr/%s/repmgr-main.conf node status' % (pg_version, pg_version))
            result = cmd.stdout.strip()

        assert len(result) > 0, \
            "repmgr command node status failed"

def test_setup_repmgr_node_status_debian():
    if os_family() != 'Debian':
        pytest.skip()

    pg_user = 'postgres'
    pg_group = 'postgres'

    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]

    for host in hosts:
        with host.sudo(pg_user):
            cmd = host.run('repmgr -f /etc/repmgr.conf node status')
            result = cmd.stdout.strip()

        assert len(result) > 0, \
            "repmgr command node status failed"

def test_setup_repmgr_node_check_redhat():
    if os_family() != 'RedHat':
        pytest.skip()

    pg_user = 'postgres'
    pg_group = 'postgres'
    pg_version = get_pg_version()
    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]

    for host in hosts:
        with host.sudo(pg_user):
            cmd = host.run('/usr/pgsql-%s/bin/repmgr -f /etc/repmgr/%s/repmgr-main.conf node check' % (pg_version, pg_version))
            result = cmd.stdout.strip().split('\n')

        assert len(result) > 0, \
            "repmgr command node check failed"

        for line in result[1:]:
            assert 'OK' in line or 'ERROR' not in line, \
                "This repmgr command node check failed: %s" % line

def test_setup_repmgr_node_check_debian():
    if os_family() != 'Debian':
        pytest.skip()

    pg_user = 'postgres'
    pg_group = 'postgres'

    hosts = [get_primary(), get_witness()[0], get_standbys()[0]]

    for host in hosts:
        with host.sudo(pg_user):
            cmd = host.run('repmgr -f /etc/repmgr.conf node check')
            result = cmd.stdout.strip().split('\n')

        assert len(result) > 0, \
            "repmgr command node check failed"

        for line in result[1:]:
            assert 'OK' in line or 'ERROR' not in line, \
                "This repmgr command node check failed: %s" % line

