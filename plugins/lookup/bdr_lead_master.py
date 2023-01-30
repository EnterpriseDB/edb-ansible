from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: bdr_nodes
    author: Julien Tachoires
    short_description: Lookup function for BDR lead master node
    description:
      - "Retrieves the BDR lead master for a giving HA location"
    options:
      _terms:
        description: HA location name.
        required: True
"""

EXAMPLES = """
- name: Get the BDR lead master of the BDRDC1 HA location
  debug: msg="{{ lookup('bdr_lead_master', 'BDRDC1') }}"
"""

RETURN = """
_value:
  description:
    - List of BDR nodes
  type: list
  elements: dict
"""

from ansible.plugins.lookup import LookupBase

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        bdr_nodes = []
        filter_ha_location = None

        myvars = getattr(self._templar, '_available_variables', {})

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        if len(terms) > 0:
            filter_ha_location = terms[0]
        else:
            return []

        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]

            if 'bdr' not in hostvars:
                # Not a BDR node
                continue

            if 'roles' not in hostvars['bdr']:
                # No BDR role defined
                continue

            if 'lead_master' not in hostvars['bdr']['roles']:
                # Not a lead_master node
                continue

            bdr_node = dict(
                node_type='primary',
                ansible_host=hostvars['ansible_host'],
                hostname=hostvars.get(
                    'hostname', hostvars.get('ansible_hostname')
                ),
                private_ip=hostvars['private_ip'],
                inventory_hostname=hostvars['inventory_hostname'],
                ha_location=hostvars['bdr'].get('ha_location', None),
                roles=hostvars['bdr'].get('roles', ['primary']),
                upstream_node_private_ip=hostvars['bdr'].get(
                    'upstream_node_private_ip', None
                ),
            )

            if filter_ha_location == bdr_node['ha_location']:
                bdr_nodes.append(bdr_node)

        return bdr_nodes
