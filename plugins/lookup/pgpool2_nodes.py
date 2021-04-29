from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pgpool2_nodes
    author: Julien Tachoires
    short_description: Lookup for PgPoolII nodes
    description:
      - "Lookup for PgPoolII nodes"
    options:
      _terms:
        description: Private IP of the primary PG node.
        required: False
      default:
        description: Do not filter on primary private IP.
"""

EXAMPLES = """
- name: Show pgpool2 nodes
  debug: msg="{{ lookup('pgpool2_nodes') }}"
"""

RETURN = """
_value:
  description:
    - List of PgPoolII nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip,
            primary_private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        nodes = []
        if len(variables['groups'].get('pgpool2', [])) == 0:
            return []

        myvars = getattr(self._templar, '_available_variables', {})
        # Inventory hostname
        inventory_hostname= variables['inventory_hostname']

        primary_private_ip = terms[0] if len(terms) > 0 else None

        # Lookup for pgpool2 nodes with a matching primary_private_ip
        for host in variables['groups']['pgpool2']:
            hostvars = myvars['hostvars'][host]

            # Ignore current item if primary_private_ip is set and does not
            # match
            if (primary_private_ip is not None and
                    hostvars.get('primary_private_ip', None) != primary_private_ip):
                continue

            nodes.append(
                dict(
                    node_type='pgpool2',
                    ansible_host=hostvars['ansible_host'],
                    private_ip=hostvars['private_ip'],
                    hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                    inventory_hostname=hostvars['inventory_hostname'],
                    primary_private_ip=hostvars.get('primary_private_ip', None),
                )
            )
        return nodes
