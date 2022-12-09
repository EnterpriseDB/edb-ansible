from __future__ import absolute_import, division, print_function

from ansible.plugins.lookup import LookupBase

__metaclass__ = type

DOCUMENTATION = """
    name: supported_roles
    author: Julien Tachoires
    short_description: Get the list of the supported roles by the current host
    description:
      - "Get the list of the supported roles byt the current host, based on its
        groups and attributes."
"""

EXAMPLES = """
- name: Get the supported roles by the current host
  debug: msg="{{ lookup('supported_roles') }}"
"""

RETURN = """
_value:
  description:
    - List of role name
  type: list
  elements:
    - string
"""


GROUP_ROLES = {
    'primary': [
        'setup_repo',
        'install_dbserver',
        'manage_extension',
        'init_dbserver',
        'manage_dbserver'
        'autotuning',
        'setup_repmgr',
        'manage_dbpatches',
    ],
    'standby': [
        'setup_repo',
        'install_dbserver',
        'manage_extension',
        'setup_replication',
        'manage_dbserver',
        'autotuning',
        'setup_repmgr',
        'manage_dbpatches',
        'manage_extension',
    ],
    'pemserver': [
        'setup_repo',
        'install_dbserver',
        'init_dbserver',
        'manage_dbserver',
        'setup_pemserver',
        'autotuning'
    ],
    'pgbouncer': [
        'setup_repo',
        'setup_pgbouncer',
        'manage_pgbouncer'
    ],
    "standby": [
        "setup_repo",
        "install_dbserver",
        "manage_extension",
        "setup_replication",
        "manage_dbserver",
        "autotuning",
        "setup_repmgr",
        "manage_dbpatches",
    ],
    "pemserver": [
        "setup_repo",
        "install_dbserver",
        "init_dbserver",
        "manage_dbserver",
        "setup_pemserver",
        "autotuning",
    ],
    "pgbouncer": ["setup_repo", "setup_pgbouncer", "manage_pgbouncer"],
    "pgpool2": ["setup_repo", "setup_pgpool2", "manage_pgpool2"],
    "barmanserver": ["setup_repo", "setup_barmanserver", "install_dbserver"],
    "dbt2_driver": [
        "setup_repo",
        "setup_dbt2_driver",
    ],
    "dbt2_client": [
        "setup_dbt2_client",
    ],
    "hammerdbserver": ["setup_hammerdbserver"],
    "witness": [
        "setup_repo",
        "install_dbserver",
        "setup_repmgr",
        "manage_dbpatches",
    ],
    "proxy": [
        "setup_repo",
        "setup_harp_proxy",
    ],
    "pgbackrestserver": [
        "setup_repo",
        "setup_pgbackrestserver",
    ],
}


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        supported_roles = []
        # Inventory hostname
        hostname = variables["inventory_hostname"]

        myvars = getattr(self._templar, "_available_variables", {})
        hostvars = myvars["hostvars"][hostname]

        # BDR roles available
        bdr_roles = ["primary", "read_only", "lead_master", "witness"]

        for group in variables["group_names"]:
            supported_roles = list(
                set(supported_roles) | set(GROUP_ROLES.get(group, []))
            )
            # Special case for the primary or standby nodes when the host
            # variable pgbouncer is set to true.
            if group in ["primary", "standby"] and hostvars.get("pgbouncer", False):
                supported_roles = list(
                    set(supported_roles) | set(["setup_pgbouncer", "manage_pgbouncer"])
                )
            # Special case for the primary, standby or proxy nodes when the
            # host variable pem_agent is set to true.
            if group in ["primary", "standby", "proxy", "barmanserver"] and (
                hostvars.get("pem_agent", False)
                or hostvars.get("pem_agent_remote", False)
            ):
                supported_roles = list(set(supported_roles) | set(["setup_pemagent"]))
            # Special case for the pemserver, primary or standby nodes when
            # the host variable barman is set to true.
            if group in ["pemserver", "primary", "standby"] and hostvars.get(
                "barman", False
            ):
                supported_roles = list(set(supported_roles) | set(["setup_barman"]))
            # Special case for the primary nodes when the host variable
            # dbt2 is set to true.
            if group in ["primary"] and hostvars.get("dbt2", False):
                supported_roles = list(set(supported_roles) | set(["setup_dbt2"]))
            # Special case for the primary nodes when the host variable
            # dbt3 is set to true.
            if group in ["primary"] and hostvars.get("dbt3", False):
                supported_roles = list(set(supported_roles) | set(["setup_dbt3"]))
            # Special case for the primary nodes when the host variable
            # dbt7 is set to true.
            if group in ["primary"] and hostvars.get("dbt7", False):
                supported_roles = list(set(supported_roles) | set(["setup_dbt7"]))
            # Special case for the primary nodes when the host variable
            # hammerdb is set to true.
            if group in ["primary"] and hostvars.get("hammerdb", False):
                supported_roles = list(set(supported_roles) | set(["setup_hammerdb"]))
            # Special case for the witness nodes when the host variable
            # init_dbserver is set to true. This is required for repmgr: the
            # witness node must have a dedicated database instance running.
            if group in ["witness"] and hostvars.get("init_dbserver", False):
                supported_roles = list(set(supported_roles) | set(["init_dbserver"]))

            # BDR cases
            if group in ["primary"] and hostvars.get("bdr"):
                # BDR nodes are part of the primary group and must have the
                # 'bdr' hostvar defined as well as the 'bdr.roles' list
                # should contain at least one of the BDR roles available
                # (primary, read_only, lead_master, and witness).
                if len(set(bdr_roles) & set(hostvars["bdr"].get("roles", []))):
                    supported_roles = list(set(supported_roles) | set(["setup_bdr"]))
            # etcd case
            if group in ["primary", "proxy", "barmanserver"] and hostvars.get("bdr"):
                # etcd can be deployed on BDR nodes, proxy nodes and barman
                # nodes. The etcd hostvar must be set to true.
                if hostvars["bdr"].get("etcd", False):
                    supported_roles = list(set(supported_roles) | set(["setup_etcd"]))
            # Harp manager case
            if group in ["primary"] and hostvars.get("bdr"):
                # Harp manager is deployed on the primary BDR nodes when the
                # hostvar harp_manager is set to true.
                host_bdr_roles = hostvars["bdr"].get("roles", [])
                harp_manager = hostvars["bdr"].get("harp_manager", False)
                if len(set(["primary"]) & set(host_bdr_roles)) and harp_manager:  # noqa
                    supported_roles = list(
                        set(supported_roles) | set(["setup_harp_manager"])
                    )
            # Special case for the primary or standby nodes when the host
            # variable pgbackrest is set to true.
            if group in ["primary", "standby"] and hostvars.get("pgbackrest", False):
                supported_roles = list(set(supported_roles) | set(["setup_pgbackrest"]))
        return supported_roles
