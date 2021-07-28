from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: dbt2_client
    author: Mark Wong
    short_description: Lookup DBT-2 client server, based on its private_ip
    description:
      - "Lookup DBT-2 client server, based on its private_ip"
    options:
      _terms:
        description: Private IP of the DBT-2 client server.
        required: False
      default:
        description:dbt2_client_private_ip of the current node.
"""

EXAMPLES = """
- name: Show DBT-2 client server information
  debug: msg="{{ lookup('dbt2_client') }}"
"""

RETURN = """
_value:
  description:
    - List of DBT-2 client server nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        myvars = getattr(self._templar, '_available_variables', {})
        inventory_hostname = variables['inventory_hostname']

        # If no terms, we'll used the current DBT-2 client private IP
        if len(terms) == 0:
            if 'dbt2_client' not in myvars['hostvars'][inventory_hostname]:
                # dbt2_client not set, return None
                return []
            dbt2_client = myvars['hostvars'][inventory_hostname]['dbt2_client']
        else:
            dbt2_client = terms[0]

        # If no dbt2client found in the inventory file, just return None
        if 'dbt2client' not in variables['groups']:
            return []
        if len(variables['groups']['dbt2client']) == 0:
            return []

        # Lookup for DBT-2 clients with a matching private_ip
        for host in variables['groups']['dbt2client']:
            hostvars = myvars['hostvars'][host]

            if hostvars['private_ip'] != dbt2_client:
                continue

            return [
                dict(
                    node_type='dbt2client',
                    ansible_host=hostvars['ansible_host'],
                    hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                    private_ip=hostvars['private_ip'],
                    inventory_hostname=hostvars['inventory_hostname']
                )
            ]
