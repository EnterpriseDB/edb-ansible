from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: repmgr_nodes
    author: Julien Tachoires
    short_description: Lookup for repmgr nodes
    description:
      - "Retrieves the repmgr nodes list, based on node's private IP"
    options:
      _terms:
        description: The private IP of one member of the repmgr cluster.
        required: False
      default:
        description: The private IP of the current node is used.
"""

EXAMPLES = """
- name: Show all members of the repmgr cluster that the current node is part of
  debug: msg="{{ lookup('repmgr_nodes') }}"

- name: Show all members of the repmgr cluster that the {{ primary_private_ip }} is part of
  debug: msg="{{ lookup('repmgr_nodes', primary_private_ip) }}"
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

        repmgr_clusters = {}
        repmgr_standbys = {}
        repmgr_witnesses = {}
        repmgr_primary_map = {}
        node_id = {}

        myvars = getattr(self._templar, '_available_variables', {})

        # If no terms, we'll used the current private IP
        if len(terms) == 0:
            node_private_ip = myvars['hostvars'][variables['inventory_hostname']]['private_ip']  # noqa
        else:
            node_private_ip = terms[0]

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        # Initiate repmgr_clusters and repmgr_primary_map for each primary node we have
        # in the inventory.
        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]
            private_ip = hostvars['private_ip']

            node_id[private_ip] = 1
            repmgr_clusters[private_ip] = []
            repmgr_clusters[private_ip].append(
                dict(
                    node_type='primary',
                    id=node_id[private_ip],
                    ansible_host=hostvars.get('ansible_host'),
                    hostname=hostvars.get('hostname',
                                          hostvars.get('ansible_hostname')),
                    private_ip=hostvars['private_ip'],
                    upstream_node_private_ip=None,
                    replication_type=None,
                    inventory_hostname=hostvars['inventory_hostname']
                )
            )
            repmgr_primary_map[private_ip] = private_ip

        # Populate repmgr_standbys dict if we have standby nodes in the inventory
        if 'standby' in variables['groups']:
            for host in variables['groups']['standby']:
                hostvars = myvars['hostvars'][host]
                node_id[hostvars['upstream_node_private_ip']] += 1
                repmgr_standbys[host] = dict(
                    node_type='standby',
                    id=node_id[hostvars['upstream_node_private_ip']],
                    ansible_host=hostvars.get('ansible_host'),
                    hostname=hostvars.get('hostname',
                                          hostvars.get('ansible_hostname')),
                    private_ip=hostvars['private_ip'],
                    upstream_node_private_ip=hostvars['upstream_node_private_ip'],
                    replication_type=hostvars.get('replication_type',
                                                  'asynchronous'),
                    inventory_hostname=hostvars['inventory_hostname']
                )

        repmgr_standbys_len = len(repmgr_standbys.keys())

        # Populate repmgr_witnesses dict if we have witness nodes in the inventory
        if 'witness' in variables['groups']:
            for host in variables['groups']['witness']:
                hostvars = myvars['hostvars'][host]
                node_id[hostvars['upstream_node_private_ip']] += 1
                repmgr_witnesses[host] = dict(
                    node_type='witness',
                    id=node_id[hostvars['upstream_node_private_ip']],
                    ansible_host=hostvars.get('ansible_host'),
                    hostname=hostvars.get('hostname',
                                          hostvars.get('ansible_hostname')),
                    private_ip=hostvars['private_ip'],
                    upstream_node_private_ip=hostvars['upstream_node_private_ip'],
                    replication_type=None,
                    inventory_hostname=hostvars['inventory_hostname']
                )

        repmgr_witnesses_len = len(repmgr_witnesses.keys())

        # Append the standby nodes into the right repmgr_clusters item, based on
        # standby's upstream node.
        while repmgr_standbys_len != 0:

            for k in list(repmgr_standbys.keys()):
                sby = repmgr_standbys[k]

                if sby['upstream_node_private_ip'] in repmgr_primary_map:
                    upstream_private_ip = sby['upstream_node_private_ip']
                    primary_private_ip = repmgr_primary_map[upstream_private_ip]
                    repmgr_primary_map[sby['private_ip']] = primary_private_ip
                    repmgr_clusters[primary_private_ip].append(sby)
                    del(repmgr_standbys[k])

            # Case when at least one host has not been handled in this loop
            # iteration.
            if repmgr_standbys_len == len(repmgr_standbys.keys()):
                raise AnsibleError(
                    "Inventory error with the following standbys nodes %s. "
                    "Upstream node is not configured or not found"
                    % [s for s in repmgr_standbys.keys()]
                )

            repmgr_standbys_len = len(repmgr_standbys.keys())

        # Append witness nodes into the right repmgr_clusters item, based on
        # witness's upstream node.
        while repmgr_witnesses_len != 0:

            for k in list(repmgr_witnesses.keys()):
                wit = repmgr_witnesses[k]

                if wit['upstream_node_private_ip'] in repmgr_primary_map:
                    upstream_private_ip = wit['upstream_node_private_ip']
                    primary_private_ip = repmgr_primary_map[upstream_private_ip]
                    repmgr_primary_map[wit['private_ip']] = primary_private_ip
                    repmgr_clusters[primary_private_ip].append(wit)
                    del(repmgr_witnesses[k])

            # Case when at least one host has not been handled in this loop
            # iteration.
            if repmgr_witnesses_len == len(repmgr_witnesses.keys()):
                raise AnsibleError(
                    "Inventory error with the following witness nodes %s. "
                    "Upstream node is not configured or not found"
                    % [s for s in repmgr_witnesses.keys()]
                )

            repmgr_witnesses_len = len(repmgr_witnesses.keys())


        if node_private_ip in repmgr_primary_map:
            # Current node is part of one of the SR clusters found
            return repmgr_clusters[repmgr_primary_map[node_private_ip]]
        else:
            primary_private_ips = list(repmgr_clusters.keys())
            # If the current node is not part of any repmgr cluster found, but,
            # only one repmgr cluster has been found, then we return this repmgr
            # cluster because there is no doubt.
            if len(primary_private_ips) == 1:
                return repmgr_clusters[primary_private_ips[0]]
            else:
                raise AnsibleError(
                    "Unable to find the repmgr cluster topology because multiple "
                    "repmgr clusters were found and this current node does not "
                    "appear to be part of any of them"
                )
