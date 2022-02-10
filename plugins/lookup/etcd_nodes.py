from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: etcd_nodes
    author: Julien Tachoires
    short_description: Lookup function for etcd nodes
    description:
      - "Retrieves the etcd nodes list"
    options:
      _terms:
        description: HA location name.
        required: False
      default:
        description: All etcd nodes are returned, no filter applied.
"""

EXAMPLES = """
- name: Show all members of the etcd clusters
  debug: msg="{{ lookup('etcd_nodes') }}"

- name: Show all members of the etcd cluster located in the BDRDC1 HA location
  debug: msg="{{ lookup('etcd_nodes', 'BDRDC1') }}"
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
        filter_ha_location = None

        myvars = getattr(self._templar, '_available_variables', {})

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        if len(terms) > 0:
            filter_ha_location = terms[0]

        # etcd can be deployed on BDR, barman and proxy nodes
        for group in ('primary', 'barmanserver', 'proxy'):

            if group not in variables['groups']:
                continue

            for host in variables['groups'][group]:
                hostvars = myvars['hostvars'][host]

                if 'bdr' not in hostvars:
                    # Not a node being part of the BDR architecture
                    continue

                if not hostvars['bdr'].get('etcd'):
                    # The bdr.etcd hostvar not set to true
                    continue

                etcd_node = dict(
                    ansible_host=hostvars['ansible_host'],
                    hostname=hostvars.get(
                        'hostname', hostvars.get('ansible_hostname')
                    ),
                    private_ip=hostvars['private_ip'],
                    inventory_hostname=hostvars['inventory_hostname'],
                    ha_location=hostvars['bdr'].get('ha_location', None),
                )

                if filter_ha_location is not None:
                    if filter_ha_location == etcd_node['ha_location']:
                        etcd_nodes.append(etcd_node)
                else:
                    etcd_nodes.append(etcd_node)

        return etcd_nodes
