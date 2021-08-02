from __future__ import (absolute_import, division, print_function)
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

from ansible.plugins.lookup import LookupBase

GROUP_ROLES = {
    'primary': [
        'setup_repo',
        'install_dbserver',
        'init_dbserver',
        'manage_dbserver',
        'setup_efm',
        'autotuning'
    ],
    'standby': [
        'setup_repo',
        'install_dbserver',
        'setup_replication',
        'manage_dbserver',
        'setup_efm',
        'autotuning'
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
    'pgpool2': [
        'setup_repo',
        'setup_pgpool2',
        'manage_pgpool2'
    ],
    'barmanserver': [
        'setup_repo',
        'setup_barmanserver',
        'install_dbserver'
    ],
    'dbt2_driver': [
        'setup_dbt2_driver'
    ],
    'dbt2_client': [
        'setup_dbt2_client'
    ],
    'hammerdbserver': [
        'setup_hammerdbserver'
    ]
}


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        supported_roles = []
        # Inventory hostname
        hostname = variables['inventory_hostname']

        myvars = getattr(self._templar, '_available_variables', {})

        for group in variables['group_names']:
            supported_roles = list(
                set(supported_roles)
                | set(GROUP_ROLES.get(group, []))
            )
            # Special case for the primary or standby nodes when the host
            # variable pgbouncer is set to true.
            if (group in ['primary', 'standby']
                    and myvars['hostvars'][hostname].get('pgbouncer', False)):
                supported_roles = list(
                    set(supported_roles)
                    | set(['setup_pgbouncer', 'manage_pgbouncer'])
                )
            # Special case for the primary or standby nodes when the
            # host variable pem_agent is set to true.
            if (group in ['primary', 'standby']
                    and myvars['hostvars'][hostname].get('pem_agent', False)):
                supported_roles = list(
                    set(supported_roles)
                    | set(['setup_pemagent'])
                )
            # Special case for the pemserver, primary or standby nodes when
            # the host variable barman is set to true.
            if (group in ['pemserver', 'primary', 'standby']
                    and myvars['hostvars'][hostname].get('barman', False)):
                supported_roles = list(
                    set(supported_roles)
                    | set(['setup_barman'])
                )
            # Special case for the primary nodes when the host variable
            # dbt2 is set to true.
            if (group in ['primary']
                    and myvars['hostvars'][hostname].get('dbt2', False)):
                supported_roles = list(
                    set(supported_roles)
                    | set(['setup_dbt2'])
                )
            # Special case for the primary nodes when the host variable
            # hammerdb is set to true.
            if (group in ['primary']
                    and myvars['hostvars'][hostname].get('hammerdb', False)):
                supported_roles = list(
                    set(supported_roles)
                    | set(['setup_hammerdb'])
                )
        return supported_roles
