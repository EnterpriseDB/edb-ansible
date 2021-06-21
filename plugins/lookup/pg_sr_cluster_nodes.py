from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pg_sr_cluster_nodes
    author: Julien Tachoires
    short_description: Lookup Postgres SR cluster nodes
    description:
      - "Retrieves the Postgres streaming replication nodes list, based on
        node's private IP"
    options:
      _terms:
        description: The private IP of one member of the SR cluster.
        required: False
      default:
        description: The private IP of the current node is used.
"""

EXAMPLES = """
- name: Show all members of the SR cluster that the current node is part of
  debug: msg="{{ lookup('pg_sr_cluster_nodes') }}"

- name: Show all members of the SR cluster that the {{ primary_private_ip }} is part of
  debug: msg="{{ lookup('pg_sr_cluster_nodes', primary_private_ip) }}"
"""

RETURN = """
_value:
  description:
    - List of Postgres nodes
  type: list
  elements: dict
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        pg_clusters = {}
        pg_standbys = {}
        pg_primary_map = {}

        myvars = getattr(self._templar, '_available_variables', {})

        # If no terms, we'll used the current private IP
        if len(terms) == 0:
            node_private_ip = myvars['hostvars'][variables['inventory_hostname']]['private_ip']
        else:
            node_private_ip = terms[0]

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        # Initiate pg_clusters and pg_primary_map for each primary node we have
        # in the inventory.
        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]
            private_ip = hostvars['private_ip']

            pg_clusters[private_ip] = []
            pg_clusters[private_ip].append(
                dict(
                    node_type='primary',
                    ansible_host=hostvars['ansible_host'],
                    hostname=hostvars.get('hostname',
                                          hostvars.get('ansible_hostname')),
                    private_ip=hostvars['private_ip'],
                    upstream_node_private_ip=None,
                    replication_type=None,
                    inventory_hostname=hostvars['inventory_hostname']
                )
            )
            pg_primary_map[private_ip] = private_ip

        # Populate pg_standbys dict if we have standby nodes in the inventory
        if 'standby' in variables['groups']:
            for host in variables['groups']['standby']:
                hostvars = myvars['hostvars'][host]
                pg_standbys[host] = dict(
                    node_type='standby',
                    ansible_host=hostvars['ansible_host'],
                    hostname=hostvars.get('hostname',
                                          hostvars.get('ansible_hostname')),
                    private_ip=hostvars['private_ip'],
                    upstream_node_private_ip=hostvars['upstream_node_private_ip'],
                    replication_type=hostvars.get('replication_type',
                                                  'asynchronous'),
                    inventory_hostname=hostvars['inventory_hostname']
                )

        pg_standbys_len = len(pg_standbys.keys())

        # Append the standby nodes into the right pg_clusters item, based on
        # standby's upstream node.
        while pg_standbys_len != 0:

            for k in list(pg_standbys.keys()):
                sby = pg_standbys[k]

                if sby['upstream_node_private_ip'] in pg_primary_map:
                    upstream_private_ip = sby['upstream_node_private_ip']
                    primary_private_ip = pg_primary_map[upstream_private_ip]
                    pg_primary_map[sby['private_ip']] = primary_private_ip
                    pg_clusters[primary_private_ip].append(sby)
                    del(pg_standbys[k])

            # Case when at least one host has not been handled in this loop
            # iteration.
            if pg_standbys_len == len(pg_standbys.keys()):
                raise AnsibleError(
                    "Inventory error with the following standbys nodes %s. "
                    "Upstream node is not configured or not found"
                    % [s for s in pg_standbys.keys()]
                )

            pg_standbys_len = len(pg_standbys.keys())


        if node_private_ip in pg_primary_map:
            # Current node is part of one of the SR clusters found
            return pg_clusters[pg_primary_map[node_private_ip]]
        else:
            primary_private_ips = list(pg_clusters.keys())
            # If the current node is not part of any SR cluster found, but,
            # only one SR cluster has been found, then we return this SR
            # cluster because there is no doubt.
            if len(primary_private_ips) == 1:
                return pg_clusters[primary_private_ips[0]]
            else:
                raise AnsibleError(
                    "Unable to find the SR cluster topology because multiple "
                    "SR clusters were found and this current node does not "
                    "appear to be part of any of them"
                )
