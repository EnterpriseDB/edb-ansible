from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: barman_server
    author: Julien Tachoires
    short_description: Lookup Barman server, based on its private_ip
    description:
      - "Lookup Barman server, based on its private_ip"
    options:
      _terms:
        description: Private IP of the Barman server.
        required: False
      default:
        description: barman_server_private_ip of the current node.
"""

EXAMPLES = """
- name: Show Barman server informations
  debug: msg="{{ lookup('barman_server') }}"
"""

RETURN = """
_value:
  description:
    - List of Barman server nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        myvars = getattr(self._templar, '_available_variables', {})
        inventory_hostname = variables['inventory_hostname']

        # If no terms, we'll used the current Barman server private IP
        if len(terms) == 0:
            if 'barman_server_private_ip' not in myvars['hostvars'][inventory_hostname]:
                # barman_server_private_ip not set, return None
                return []
            barman_server_private_ip = myvars['hostvars'][inventory_hostname]['barman_server_private_ip']
        else:
            barman_server_private_ip = terms[0]

        # If no barmanserver found in the inventory file, just return None
        if 'barmanserver' not in variables['groups']:
            return []
        if len(variables['groups']['barmanserver']) == 0:
            return []

        # Lookup for barman servers with a matching private_ip
        for host in variables['groups']['barmanserver']:
            hostvars = myvars['hostvars'][host]

            if hostvars['private_ip'] != barman_server_private_ip:
                continue

            return [
                dict(
                    node_type='barmanserver',
                    ansible_host=hostvars['ansible_host'],
                    hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                    private_ip=hostvars['private_ip'],
                    inventory_hostname=hostvars['inventory_hostname']
                )
            ]
