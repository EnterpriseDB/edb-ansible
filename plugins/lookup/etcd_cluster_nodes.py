from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: etcd_cluster_nodes
    author: Julien Tachoires
    co-author: Vibhor Kumar
    short_description: Lookup function for etcd nodes
    description:
      - "Retrieves the etcd nodes list"
    options:
      _terms:
        description: etcd_cluster_name variable.
        required: False
      default:
        description: All etcd nodes are returned, no filter applied.
"""

EXAMPLES = """
- name: Show all members of the etcd clusters
  debug: msg="{{ lookup('etcd_cluster_nodes') }}"

- name: Show all members of the etcd cluster located in the named cluster nodes
  debug: msg="{{ lookup('etcd_cluster_nodes', 'patroni-etcd') }}"
"""

RETURN = """
_value:
  description:
    - List of etcd nodes
  type: list
  elements: dict
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        etcd_nodes = []
        filter_etcd_cluster_name = None

        myvars = getattr(self._templar, '_available_variables', {})
        # inventory hostname
        ihn = variables['inventory_hostname']

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        # # If no terms, we'll used the current hosts etcd_cluster_name if defined
        if len(terms) == 0:
            if 'etcd_cluster_name' in myvars['hostvars'][ihn]:
                filter_etcd_cluster_name = myvars['hostvars'][ihn]['etcd_cluster_name']

        if len(terms) > 0:
            filter_etcd_cluster_name = terms[0]

        # etcd can be deployed on BDR, barman and proxy nodes
        for group in ['primary', 'standby', 'pemserver', 'pgbouncer', 'pgpool2',
                      'barmanserver', 'witness', 'proxy', 'pgbackrestserver']:

            if group not in variables['groups']:
                continue

            for host in variables['groups'][group]:
                hostvars = myvars['hostvars'][host]

                hv = myvars['hostvars'][host]

                if 'etcd' not in hostvars:
                    # Not a node being part of the etcd
                    continue

                if hostvars.get('etcd'):
                    if 'etcd_cluster_name' not in hostvars:
                        continue
                    
                    if hv['etcd_cluster_name'] != filter_etcd_cluster_name:
                        continue

                    etcd_node = dict(
                        ansible_host=hostvars['ansible_host'],
                        hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                        private_ip=hostvars['private_ip'],
                        inventory_hostname=hostvars['inventory_hostname'],
                        etcd_cluster_name=hostvars.get('etcd_cluster_name', hostvars['etcd_cluster_name']),
                    )

                    etcd_nodes.append(etcd_node)

        return etcd_nodes
