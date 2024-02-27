from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pgBackRest_server
    author: Julien Tachoires
    short_description: Lookup pgBackRest server, based on its private_ip
    description:
      - "Lookup pgBackRest server, based on its private_ip"
    options:
      _terms:
        description: Private IP of the pgBackRest server.
        required: False
      default:
        description: pgbackrest_server_private_ip of the current node.
"""

EXAMPLES = """
- name: Show pgBackRest server informations
  debug: msg="{{ lookup('pgbackrest_server') }}"
"""

RETURN = """
_value:
  description:
    - List of pgBackRest server nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        myvars = getattr(self._templar, '_available_variables', {})
        inventory_hostname = variables['inventory_hostname']

        # If no terms, we'll used the current pgBackRest server private IP
        if len(terms) == 0:
            if 'pgbackrest_server_private_ip' not in myvars['hostvars'][inventory_hostname]:
                # pgbackrest_server_private_ip not set, return None
                return []
            pgbackrest_server_private_ip = myvars['hostvars'][inventory_hostname]['pgbackrest_server_private_ip']
        else:
            pgbackrest_server_private_ip = terms[0]

        # If no pgbackrestserver found in the inventory file, just return None
        if 'pgbackrestserver' not in variables['groups']:
            return []
        if len(variables['groups']['pgbackrestserver']) == 0:
            return []

        # Lookup for pgbackrest servers with a matching private_ip
        for host in variables['groups']['pgbackrestserver']:
            hostvars = myvars['hostvars'][host]

            if hostvars['private_ip'] != pgbackrest_server_private_ip:
                continue

            return [
                dict(
                    node_type='pgbackrestserver',
                    ansible_host=hostvars.get('ansible_host'),
                    hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                    private_ip=hostvars['private_ip'],
                    inventory_hostname=hostvars['inventory_hostname']
                )
            ]
