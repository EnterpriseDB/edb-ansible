import json
import os

import testinfra
import yaml

# Path to the file containing ansible variables for the role:
# <role_name>/vars.json
HYPERSQL_ANSIBLE_VARS = os.getenv("HYPERSQL_ANSIBLE_VARS")
# Operating system name of the containers
HYPERSQL_OS_TYPE = os.getenv("HYPERSQL_OS_TYPE", "rocky8")
# Path to the ansible inventory file: <role_name>/inventory.yml
HYPERSQL_INVENTORY = os.getenv("HYPERSQL_INVENTORY")
# Postgres version
HYPERSQL_PG_VERSION = os.getenv("HYPERSQL_PG_VERSION").split('.')[0]
# Postgres type
HYPERSQL_PG_TYPE = os.getenv("HYPERSQL_PG_TYPE")
# SSH parameters
HYPERSQL_SSH_USER = os.getenv("HYPERSQL_SSH_USER", "root")
HYPERSQL_SSH_KEY = os.getenv("HYPERSQL_SSH_KEY", "../.ssh/id_rsa")
HYPERSQL_SSH_CONFIG = os.getenv("HYPERSQL_SSH_CONFIG", "../.ssh/ssh_config")
# Globale variable used as a cache
HOSTS = None


def load_ansible_vars():
    """
    Loading Ansible variables from the vars.json file
    """
    with open(HYPERSQL_ANSIBLE_VARS, "r") as f:
        return json.loads(f.read())


def load_inventory():
    """
    Loading data from the inventory file
    """
    # Read the inventory file
    with open(HYPERSQL_INVENTORY, "r") as f:
        return yaml.load(f.read(), Loader=yaml.Loader)


def get_hosts(group_name):
    """
    Returns the list of testinfra host instances, based on Ansible group name
    """
    global HOSTS

    inventory_data = load_inventory()
    children = inventory_data["all"]["children"]

    if group_name not in children:
        HOSTS = []
        return HOSTS

    nodes = []
    for host, attrs in children[group_name]["hosts"].items():
        nodes.append(
            testinfra.get_host(
                "paramiko://%s@%s:22" % (HYPERSQL_SSH_USER, attrs["ansible_host"]),
                ssh_identity_file=HYPERSQL_SSH_KEY,
                ssh_config=HYPERSQL_SSH_CONFIG,
            )
        )
    HOSTS = nodes
    return HOSTS


def get_os():
    return HYPERSQL_OS_TYPE


def get_pg_version():
    return HYPERSQL_PG_VERSION


def os_family():
    if (
        get_os().startswith("centos")
        or get_os().startswith("rocky")
        or get_os().startswith("oraclelinux")
    ):
        return "RedHat"
    elif get_os().startswith("debian") or get_os().startswith("ubuntu"):
        return "Debian"
    else:
        return "unknown"


def get_pg_type():
    return HYPERSQL_PG_TYPE


def get_primary():
    return get_hosts("primary")[0]


def get_pemserver():
    return get_hosts("pemserver")[0]


def get_barmanserver():
    return get_hosts("barmanserver")[0]


def get_pgbackrestserver():
    return get_hosts("pgbackrestserver")[0]


def get_pg_nodes():
    for group in ("primary", "standby", "pemserver"):
        for host in get_hosts(group):
            yield (group, host)


def get_pg_cluster_nodes():
    for group in ("primary", "standby"):
        for host in get_hosts(group):
            yield (group, host)


def get_standbys():
    return get_hosts("standby")


def get_pgpool2():
    return get_hosts("pgpool2")


def get_pgbouncer():
    return get_hosts("pgbouncer")


def get_witness():
    return get_hosts("witness")


def get_hammerdb():
    return get_hosts("hammerdbserver")


def get_dbt2_driver():
    return get_hosts("dbt2_driver")


def get_dbt2_client():
    return get_hosts("dbt2_client")


def get_pg_unix_socket_dir():
    pg_type = get_pg_type()
    pg_version = get_pg_version()
    if pg_type == "PG":
        return "/var/run/postgresql"
    elif pg_type == "EPAS":
        if os_family() == "RedHat":
            return "/var/run/edb/as%s" % pg_version
        elif os_family() == "Debian":
            return "/var/run/edb-as"


def get_pg_profile_dir():
    pg_type = get_pg_type()
    if pg_type == "PG":
        if os_family() == "RedHat":
            return "/var/lib/pgsql"
        elif os_family() == "Debian":
            return "/var/lib/postgresql"
    elif pg_type == "EPAS":
        if os_family() == "RedHat":
            return "/var/lib/edb/"
        elif os_family() == "Debian":
            return "/var/lib/edb-as"


def get_pgbouncer_pid_file():
    pg_type = get_pg_type()
    if pg_type == "PG":
        if os_family() == "RedHat":
            return "/run/pgbouncer/pgbouncer.pid"
        elif os_family() == "Debian":
            return "/var/run/pgbouncer/pgbouncer.pid"
    elif pg_type == "EPAS":
        if os_family() == "RedHat":
            return "/run/edb/pgbouncer1.17/edb-pgbouncer-1.17.pid"
        elif os_family() == "Debian":
            return "/var/run/edb/pgbouncer1.17/edb-pgbouncer-1.17.pid"


def get_pgbouncer_auth_file():
    pg_type = get_pg_type()
    if pg_type == "PG":
        if os_family() == "RedHat":
            return "/etc/pgbouncer/userlist.txt"
        elif os_family() == "Debian":
            return "/etc/pgbouncer/userlist.txt"
    elif pg_type == "EPAS":
        if os_family() == "RedHat":
            return "/etc/edb/pgbouncer1.17/userlist.txt"
        elif os_family() == "Debian":
            return "/etc/edb/pgbouncer1.17/userlist.txt"
