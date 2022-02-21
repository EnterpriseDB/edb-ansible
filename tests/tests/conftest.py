import os
import json
import pytest
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


def get_pg_version():
    return EDB_PG_VERSION


def get_pg_type():
    return EDB_PG_TYPE


def get_primary():
    return get_hosts('primary')[0]


def get_pemserver():
    return get_hosts('pemserver')[0]


def get_barmanserver():
    return get_hosts('barmanserver')[0]


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


def get_pg_unix_socket_dir():
    pg_type = get_pg_type()
    pg_version = get_pg_version()
    sys_os = get_os()
    if pg_type == 'PG':
        return '/var/run/postgresql'
    elif pg_type == 'EPAS':
        if sys_os.startswith('centos') or sys_os.startswith('rocky'):
            return '/var/run/edb/as%s' % pg_version
        elif sys_os.startswith('debian') or sys_os.startswith('ubuntu'):
            return '/var/run/edb-as'

def get_pg_profile_dir():
    pg_type = get_pg_type()
    sys_os = get_os()
    if pg_type == 'PG':
        if sys_os.startswith('centos') or sys_os.startswith('rocky'):
            return '/var/lib/pgsql'
        elif sys_os.startswith('debian') or sys_os.startswith('ubuntu'):
            return '/var/lib/postgresql'
    elif pg_type == 'EPAS':
        if sys_os.startswith('centos') or sys_os.startswith('rocky'):
            return '/var/lib/edb/'
        elif sys_os.startswith('debian') or sys_os.startswith('ubuntu'):
            return '/var/lib/edb-as'
