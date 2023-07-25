import os
import json
import pytest
import re
import testinfra
import yaml


# Path to the file containing ansible variables for the role:
# <role_name>/vars.json
EDB_ANSIBLE_VARS = os.getenv('EDB_ANSIBLE_VARS')
# Operating system name of the containers
EDB_OS = os.getenv('EDB_OS', 'rocky8')
# Path to the ansible inventory file: <role_name>/inventory.yml
EDB_INVENTORY = os.getenv('EDB_INVENTORY')
# Postgres version
EDB_PG_VERSION = os.getenv('EDB_PG_VERSION')
# Postgres type
EDB_PG_TYPE = os.getenv('EDB_PG_TYPE')
# Use EDB repo
EDB_ENABLE_REPO = (os.getenv('EDB_ENABLE_REPO').lower() in ['true', '1'])
# SSH parameters
EDB_SSH_USER = os.getenv('EDB_SSH_USER', 'root')
EDB_SSH_KEY = os.getenv('EDB_SSH_KEY', '../.ssh/id_rsa')
EDB_SSH_CONFIG = os.getenv('EDB_SSH_CONFIG', '../.ssh/ssh_config')
# Globale variable used as a cache
HOSTS = None


def load_ansible_vars():
    """
    Loading Ansible variables from the vars.json file
    """
    with open(EDB_ANSIBLE_VARS, 'r') as f:
        return json.loads(f.read())


def load_inventory():
    """
    Loading data from the inventory file
    """
    # Read the inventory file
    with open(EDB_INVENTORY, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.Loader)


def get_hosts(group_name):
    """
    Returns the list of testinfra host instances, based on Ansible group name
    """
    global HOSTS

    inventory_data = load_inventory()
    children = inventory_data['all']['children']

    if group_name not in children:
        HOSTS = []
        return HOSTS

    nodes = []
    for host, attrs in children[group_name]['hosts'].items():
        nodes.append(
            testinfra.get_host(
                'paramiko://%s@%s:22' % (EDB_SSH_USER, attrs['ansible_host']),
                ssh_identity_file=EDB_SSH_KEY,
                ssh_config=EDB_SSH_CONFIG,
            )
        )
    HOSTS = nodes
    return HOSTS


def get_os():
    return EDB_OS


def get_os_version():
    return re.match(r"\D+(\d+)", EDB_OS).group(1)


def get_pg_version():
    return EDB_PG_VERSION


def os_family():
    if (get_os().startswith('centos') or get_os().startswith('rocky')
        or get_os().startswith('almalinux')
        or get_os().startswith('oraclelinux')):
        return 'RedHat'
    elif (get_os().startswith('debian') or get_os().startswith('ubuntu')):
        return 'Debian'
    elif (get_os().startswith('suse')):
        return 'Suse'
    else:
        return 'unknown'


def get_pg_type():
    return EDB_PG_TYPE


def get_primary():
    return get_hosts('primary')[0]


def get_pemserver():
    return get_hosts('pemserver')[0]


def get_barmanserver():
    return get_hosts('barmanserver')[0]


def get_pgbackrestserver():
    return get_hosts('pgbackrestserver')[0]


def get_pg_nodes():
    for group in ('primary', 'standby', 'pemserver'):
        for host in get_hosts(group):
            yield (group, host)


def get_pg_cluster_nodes():
    for group in ('primary', 'standby'):
        for host in get_hosts(group):
            yield (group, host)


def get_standbys():
    return get_hosts('standby')


def get_pgpool2():
    return get_hosts('pgpool2')


def get_pgbouncer():
    return get_hosts('pgbouncer')


def get_witness():
    return get_hosts('witness')


def get_hammerdb():
    return get_hosts('hammerdb')


def get_dbt2_driver():
    return get_hosts('dbt2_driver')


def get_dbt2_client():
    return get_hosts('dbt2_client')


def get_pg_unix_socket_dir():
    pg_type = get_pg_type()
    pg_version = get_pg_version()
    sys_os = get_os()
    if pg_type == 'PG':
        return '/var/run/postgresql'
    elif pg_type == 'EPAS':
        if os_family() == 'RedHat':
            return '/var/run/edb/as%s' % pg_version
        elif os_family() == 'Debian':
            return '/var/run/edb-as'


def get_pg_bin_dir():
    pg_type = get_pg_type()
    pg_version = get_pg_version()
    if pg_type == 'PG':
        if os_family() == 'RedHat':
            return '/usr/pgsql-%s/bin' % pg_version
        elif os_family() == 'Debian':
            return '/usr/lib/postgresql/%s/bin' % pg_version
    elif pg_type == 'EPAS':
        if os_family() == 'RedHat':
            return '/usr/edb/as%s/bin' % pg_version
        elif os_family() == 'Debian':
            return '/usr/lib/edb-as/%s/bin' % pg_version


def get_pg_profile_dir():
    pg_type = get_pg_type()
    if pg_type == 'PG':
        if os_family() == 'RedHat':
            return '/var/lib/pgsql'
        elif os_family() == 'Debian':
            return '/var/lib/postgresql'
    elif pg_type == 'EPAS':
        if os_family() == 'RedHat':
            return '/var/lib/edb/'
        elif os_family() == 'Debian':
            return '/var/lib/edb-as'


def get_pgbouncer_pid_file():
    pg_type = get_pg_type()
    if pg_type == 'PG':
        if os_family() == 'RedHat':
            return '/run/pgbouncer/pgbouncer.pid'
        elif os_family() == 'Debian':
            return '/var/run/pgbouncer/pgbouncer.pid'
    elif pg_type == 'EPAS':
        if os_family() == 'RedHat':
            return '/run/edb/pgbouncer1.17/edb-pgbouncer-1.17.pid'
        elif os_family() == 'Debian':
            return '/var/run/edb/pgbouncer1.17/edb-pgbouncer-1.17.pid'


def get_pgbouncer_auth_file():
    pg_type = get_pg_type()
    if pg_type == 'PG':
        if os_family() == 'RedHat':
            return '/etc/pgbouncer/userlist.txt'
        elif os_family() == 'Debian':
            return '/etc/pgbouncer/userlist.txt'
    elif pg_type == 'EPAS':
        if os_family() == 'RedHat':
            return '/etc/edb/pgbouncer1.17/userlist.txt'
        elif os_family() == 'Debian':
            return '/etc/edb/pgbouncer1.17/userlist.txt'


def get_enable_edb_tde():
    ansible_vars = load_ansible_vars()
    edb_enable_tde = ansible_vars.get('edb_enable_tde', False)

    return edb_enable_tde
