from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pgd_nodes
    author: Julien Tachoires & Vibhor Kumar
    short_description: Lookup function for PGD (Postgres Distributed) nodes
    description:
      - "Retrieves the PGD nodes list"
    options:
      _terms:
        description: HA location name.
        required: False
      default:
        description: All PGD nodes are returned, no filter applied.
"""

EXAMPLES = """
- name: Show all members of the PGD cluster
  debug: msg="{{ lookup('pgd_nodes') }}"

- name: Show all members of the PGD cluster located in the BDRDC1 HA location
  debug: msg="{{ lookup('pgd_nodes', 'BDRDC1') }}"
"""

RETURN = """
_value:
  description:
    - List of PGD nodes
  type: list
  elements: dict
"""

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        pgd_nodes = []
        filter_location = None

        myvars = getattr(self._templar, '_available_variables', {})

        # If no primary found in the inventory we return an empty list
        if 'primary' not in variables['groups']:
            return []

        if len(terms) > 0:
            filter_location = terms[0]
            display.vvvv("File lookup term: %s" % terms[0])

        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]

            if 'pgd' not in hostvars:
                # Not a BDR node
                continue
            display.vvvv("PGD exists!")

            pgd_node = dict(
                node_type='primary',
                ansible_host=hostvars['ansible_host'],
                hostname=hostvars.get(
                    'hostname', hostvars.get('ansible_hostname')
                ),
                private_ip=hostvars['private_ip'],
                inventory_hostname=hostvars['inventory_hostname'],
                location=hostvars.get('location', None),
                pgd_node_kind=hostvars['pgd'].get('node_kind'),
                pgd_lead_primary=hostvars['pgd'].get('lead_primary', False),
                pgd_cluster_name=hostvars['pgd'].get('cluster_name'),
                pgd_use_physical_backup=hostvars['pgd'].get('use_physical_backup', False),
                pgd_upstream_node_private_ip=hostvars['pgd'].get(
                    'upstream_node_private_ip', None
                ),
            )
            
            if filter_location is not None:
                if filter_location == pgd_node['location']:
                    pgd_nodes.append(pgd_node)
            else:
                pgd_nodes.append(pgd_node)

        return pgd_nodes
