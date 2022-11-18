import pytest

from conftest import (
    get_pg_type,
    get_pemserver,
    get_pg_version,
    get_pg_unix_socket_dir,
    os_family
)

def test_setup_pemserver_pemagent():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_pemserver()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'agent1'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pemagent user was not succesfully created"

def test_setup_pemserver_pemadmin():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_pemserver()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_user where usename = 'pemadmin'"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "pemadmin user was not succesfully created"

def test_setup_pemserver_service():
    host = get_pemserver()
    pg_version = get_pg_version()
    service = 'pemagent'

    assert host.service(service).is_running, \
        "Pemagent service not running"

    assert host.service(service).is_enabled, \
        "Pemagent service not enabled"

def test_setup_pemserver():
    host = get_pemserver()
    pg_version = get_pg_version()
    packages = ['edb-pem-server']

    if get_pg_type() == 'PG':
        if os_family() == 'RedHat':
            packages.append('sslutils_%s' % pg_version)
            packages.append('postgresql%s-contrib' % pg_version)
        elif os_family() == 'Debian':
            packages.append('postgresql-%s-sslutils' % pg_version)
            packages.append('apache2')

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % packages

def test_setup_pemserver_creation():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_pemserver()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = r"\list"
        cmd = host.run('psql -At -h %s -c "%s" postgres | grep pem' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
        "PEM database was not succesfully created"

def test_setup_pemserver_socket():
    host = get_pemserver()
    assert host.socket('tcp://0.0.0.0:8443').is_listening, \
        "PEM web interface is not listening on %s" % '0.0.0.0:8443'

def test_setup_pemserver_web_interface():
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    address = str(get_pemserver()).strip("<>").split('//')[1]
    host = get_pemserver()
    
    with host.sudo(pg_user):
        cmd = host.run(" curl --insecure -L -I https://%s/pem | grep HTTP" % address)
        result = cmd.stdout.strip()

    # Getting status code after filtering out redirection
    result = result.split('\n')
    assert '200' in result[len(result)-1], \
        "PEM web interface is not up and running."
