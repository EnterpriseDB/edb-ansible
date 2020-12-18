from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: host_supported_roles
    author: Julien Tachoires
    short_description: Set 'host_supported_roles' to the list of the supported roles.
    description:
      - "Set the variable 'host_supported_roles' to the list of the supported
         roles by this host. This list is based on the hosts's groups and on
         its host variables like 'pgbouncer' or 'pem_agent'"
'''

from ansible.plugins.vars import BaseVarsPlugin
from ansible.inventory.host import Host

GROUP_ROLES = {
    'primary': [
        'setup_repo',
        'install_dbserver',
        'init_dbserver',
        'manage_dbserver',
        'setup_efm'
    ],
    'standby': [
        'setup_repo',
        'install_dbserver',
        'setup_replication',
        'manage_dbserver',
        'setup_efm'
    ],
    'pemserver': [
        'setup_repo',
        'install_dbserver',
        'init_dbserver',
        'manage_dbserver',
        'setup_pemserver'
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
    ]
}

class VarsModule(BaseVarsPlugin):

    def get_vars(self, loader, path, entities, cache=True):
        host_supported_roles = []

        if not isinstance(entities, list):
            entities = [entities]

        super(VarsModule, self).get_vars(loader, path, entities)

        data = {'host_supported_roles': {}}

        for entity in entities:
            if not isinstance(entity, Host):
                continue

            host_vars = entity.get_vars()

            for group in host_vars['group_names']:
                host_supported_roles = list(
                    set(host_supported_roles)
                    | set(GROUP_ROLES.get(group, []))
                )
                # Special case when the primary or standby nodes where the host
                # variable pgbouncer is set to true.
                if (group in ['primary', 'standby']
                        and host_vars.get('pgbouncer', False)):
                    host_supported_roles = list(
                        set(host_supported_roles)
                        | set(['setup_pgbouncer', 'manage_pgbouncer'])
                    )
                # Special case when the primary or standby nodes where the
                # host variable pem_agent is set to true.
                if (group in ['primary', 'standby']
                        and host_vars.get('pem_agent', False)):
                    host_supported_roles = list(
                        set(host_supported_roles)
                        | set(['setup_pemagent'])
                    )

        data['host_supported_roles'] = host_supported_roles
        return data
