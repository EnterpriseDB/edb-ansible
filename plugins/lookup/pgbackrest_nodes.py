from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pgbackrest_nodes
    author: Julien Tachoires
    short_description: Lookup function returning the list of all the nodes
    description:
      - "Lookup function returning the list of all the pgBackRest nodes and their public
      and private IPs"
    options:
"""

EXAMPLES = """
- name: Show all the nodes and their IPs
  debug: msg="{{ lookup('all_nodes') }}"
"""

RETURN = """
_value:
  description:
    - List: list of dict containing the node type, public ip, hostname, the private ip and
      the inventory hostname.
  type: list
  elements: dict
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        pgbr_nodes = {}
        primary_node_ip = []

        # If no terms, we'll used the current private IP
        if len(terms) == 0:
            if 'pgbackrest_server_private_ip' not in myvars['hostvars'][inventory_hostname]:
                # pgbackrest_server_private_ip not set, return None
                return []
            pgbackrest_server_private_ip = myvars['hostvars'][variables['inventory_hostname']]['pgbackrest_server_private_ip']
        else:
            pgbackrest_server_private_ip = terms[0]

        myvars = getattr(self._templar, '_available_variables', {})

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        # find the primary pgbackrest node(s)
        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]
            pgbackrest = hostvars.get('pgbackrest', False)
            if pgbackrest:
                node = hostvars['inventory_hostname']
                if hostvars['pgbackrest_server_private_ip'] == pgbackrest_server_private_ip:
                    pgbr_nodes[node] = dict(
                        node_type='primary',
                        ansible_host=hostvars['ansible_host'],
                        hostname=hostvars.get('hostname',
                                              hostvars.get('ansible_hostname')),
                        private_ip=hostvars['private_ip'],
                        inventory_hostname=hostvars['inventory_hostname']
                    )
                    primary_node_ip.append(hostvars['private_ip'])

        # if no primary pgbackrest node, return empty list
        if len(primary_node_ip) == 0:
            raise AnsibleError(
                "Inventory error, no primary node set pgbackrest: True"
            )

        if 'standby' in variables['groups']:
        for host in variables['groups']['standby']:
            hostvars = myvars['hostvars'][host]
            pgbackrest = hostvars.get('pgbackrest', False)
            if pgbackrest:
                node = hostvars['inventory_hostname']
                if hostvars.get('pgbackrest_server_private_ip') == pgbackrest_server_private_ip:
                    if hostvars['upstream_node_private_ip'] in primary_node_ip:
                        pgbr_nodes[node] = dict(
                            node_type='standby',
                            ansible_host=hostvars['ansible_host'],
                            hostname=hostvars.get('hostname',
                                                hostvars.get('ansible_hostname')),
                            private_ip=hostvars['private_ip'],
                            inventory_hostname=hostvars['inventory_hostname']
                        )

        return pgbr_nodes

