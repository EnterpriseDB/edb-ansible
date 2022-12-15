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
- name: Show all the nodes that belong to the same pgbr cluster that the current node is part of
  debug: msg="{{ lookup('pgbackrest_nodes') }}"

- name: Show all the nodes that belong to the same pgbr cluster that the {{ private_ip }} node is part of
  debug: msg="{{ lookup('pgbackrest_nodes', private_ip) }}"
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

        # define empty list of all pgbr_nodes_private_ip
        # and resulting pgbr_nodes
        pgbr_nodes_private_ip = []
        pgbr_nodes = []

        myvars = getattr(self._templar, '_available_variables', {})
        inventory_hostname = variables['inventory_hostname']

        # get pgbr node ip's
        if len(variables['groups']['pgbackrestserver']) == 0:
            raise AnsibleError(
                "Inventory error, no pgBackRest node configured"
            )
        else:
            for host in variables['groups']['pgbackrestserver']:
                pgbr_nodes_private_ip.append(myvars['hostvars'][host]['private_ip'])

        # If no terms, we'll used the current private IP as initial node
        if len(terms) == 0:
            node_private_ip = myvars['hostvars'][inventory_hostname]['private_ip']
        else:
            node_private_ip = terms[0]

        # determine if current node is pgbr node or not
        if 'pgbackrest_server_private_ip' in myvars['hostvars'][inventory_hostname]:
            # if not define the pgbr_server_private_ip of the current node
            pgbr_server_private_ip = myvars['hostvars'][inventory_hostname]['pgbackrest_server_private_ip']
        else:
            # if current host does not have pgbr_server_ip and is not pgbr node
            # raise ansible error
            if node_private_ip not in pgbr_nodes_private_ip:
                raise AnsibleError(
                    "Inventory error, pgbackrest nodes not configured correctly"
                )
            else:
                # current node is pgbr node
                pgbr_server_private_ip = myvars['hostvars'][inventory_hostname]['private_ip']

        # find primary nodes with corresponding pgbr node as pgbackrest_server_private_ip
        # If no primary found in the inventory we return an error
        if 'primary' not in variables['groups']:
            raise AnsibleError(
                "Inventory error, no primary node configured"
            )

        # define empty list to place primary_node_ip
        primary_node_ip = []
        counter = 1

        # find the primary pgbackrest node
        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]
            pgbackrest = hostvars.get('pgbackrest', False)
            if pgbackrest:
                if hostvars['pgbackrest_server_private_ip'] == pgbr_server_private_ip:
                    pgbr_nodes.append(dict(
                        node_type='primary',
                        inventory_hostname=hostvars['inventory_hostname'],
                        ansible_host=hostvars['ansible_host'],
                        hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                        private_ip=hostvars['private_ip'],
                        index_var=str(counter)
                    ))
                    primary_node_ip.append(hostvars['private_ip'])
                    counter += 1

        # if no corresponding primary pgbackrest node, return empty list
        if len(primary_node_ip) == 0:
            raise AnsibleError(
                "Inventory error, primary node pgBackRest information not configured"
                "Check pgbackrest_node_private_ip is correct and pgbackrest: True is enabled"
            )

        # find corresponding standby nodes if they exist
        if 'standby' in variables['groups']:
            for host in variables['groups']['standby']:
                hostvars = myvars['hostvars'][host]
                pgbackrest = hostvars.get('pgbackrest', False)
                if pgbackrest:
                    # check that pgbackrest server is one we are looking for
                    if hostvars['pgbackrest_server_private_ip'] == pgbr_server_private_ip:
                        # check that upstream_node_private_ip is of the primary node already found
                        # if not raise error
                        if hostvars['upstream_node_private_ip'] not in primary_node_ip:
                            raise AnsibleError(
                                "Inventory error, primary pgbackrest_server_private_ip does not match"
                                "corresponding standby upstream_node_private_ip"
                                "Check that standby and primary pgbackrest nodes belong to same cluster"
                            )
                        else:
                            pgbr_nodes.append(dict(
                                node_type='standby',
                                inventory_hostname=hostvars['inventory_hostname'],
                                ansible_host=hostvars['ansible_host'],
                                hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                                private_ip=hostvars['private_ip'],
                                index_var=str(counter)
                            ))
                            counter += 1

        return pgbr_nodes


