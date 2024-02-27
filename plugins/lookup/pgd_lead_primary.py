from __future__ import (absolute_import, division, print_function)
__metaclass__ = type



DOCUMENTATION = """
    name: pgd_lead_primary
    author: Julien Tachoires & Vibhor Kumar
    short_description: Lookup function for PGD (Postgres Distributed) lead primary node
    description:
      - "Retrieves the PGD (Postgres Distributed) lead primary for a giving HA location"
    options:
      _terms:
        description: HA location name.
        required: True
"""

EXAMPLES = """
- name: Get the PGD lead primary of the BDRDC1 HA location
  debug: msg="{{ lookup('pgd_lead_primary', 'BDRDC1') }}"
"""

RETURN = """
_value:
  description:
    - List of PGD lead primary nodes
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
        else:
            return []

        for host in variables['groups']['primary']:
            hostvars = myvars['hostvars'][host]

            if 'pgd' not in hostvars:
                # Not a PGD node
                continue

            display.vvvv("PGD exists!")

            if 'lead_primary' not in hostvars['pgd']:
                # Not a lead_primary node
                continue
            
            display.vvvv("lead_primary in bdr roles exists")
            if not hostvars['pgd'].get('lead_primary'):
                # Not a lead_primary
                continue

            pgd_node = dict(
                node_type='primary',
                ansible_host=hostvars.get('ansible_host'),
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
            
            if filter_location == pgd_node['location']:
                pgd_nodes.append(pgd_node)

        return pgd_nodes
