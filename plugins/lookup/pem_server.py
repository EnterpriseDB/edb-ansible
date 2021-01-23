from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pem_server
    author: Julien Tachoires
    short_description: Lookup PEM server, based on its private_ip
    description:
      - "Lookup PEM server, based on its private_ip"
    options:
      _terms:
        description: Private IP of the PEM server.
        required: False
      default:
        description: pem_server_private_ip of the current node.
"""

EXAMPLES = """
- name: Show PEM server informations
  debug: msg="{{ lookup('pem_server') }}"
"""

RETURN = """
_value:
  description:
    - List of PEM server nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        myvars = getattr(self._templar, '_available_variables', {})
        # Inventory hostname
        ihn = variables['inventory_hostname']

        # If no terms, we'll used the current PEM server private IP
        if len(terms) == 0:
            if 'pem_server_private_ip' not in myvars['hostvars'][ihn]:
                # pem_server_private_ip not set, return None
                return []
            pemsrv_private_ip = myvars['hostvars'][ihn]['pem_server_private_ip']
        else:
            pemsrv_private_ip = terms[0]

        # If no pemserver found in the inventory file, just return None
        if 'pemserver' not in variables['groups']:
            return []
        if len(variables['groups']['pemserver']) == 0:
            return []

        # Lookup for pem servers with a matching private_ip
        for host in variables['groups']['pemserver']:
            hv = myvars['hostvars'][host]

            if hv['private_ip'] != pemsrv_private_ip:
                continue

            return [
                dict(
                    node_type='pemserver',
                    ansible_host=hv['ansible_host'],
                    hostname=hv.get('hostname', hv['ansible_hostname']),
                    private_ip=hv['private_ip'],
                    inventory_hostname=hv['inventory_hostname']
                )
            ]
