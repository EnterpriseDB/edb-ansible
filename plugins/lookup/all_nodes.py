from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: all_nodes
    author: Julien Tachoires
    short_description: Lookup function returning the list of all the nodes
    description:
      - "Lookup function returning the list of all the nodes and their public
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
    - List: list of dict containing the inventory hostname, the private ip and 
      the public ip.
  type: list
  elements: dict
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        all_nodes = []
        added_nodes = {}
        myvars = getattr(self._templar, '_available_variables', {})

        for group, nodes in variables['groups'].items():
            for inventory_hostname in nodes:
                if inventory_hostname in added_nodes:
                    continue
                added_nodes[inventory_hostname] = True
                hostvars = myvars['hostvars'][inventory_hostname]
                all_nodes.append(dict(
                    inventory_hostname=inventory_hostname,
                    private_ip=hostvars.get('private_ip', None),
                    public_ip=hostvars.get('public_ip', None),
                ))
        return all_nodes
