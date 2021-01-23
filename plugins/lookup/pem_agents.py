from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pem_agents
    author: Julien Tachoires
    short_description: Lookup for nodes where the PEM agent is enabled
    description:
      - "Lookup for nodes where the PEM agent is enabled, based on PEM server private_ip"
    options:
      _terms:
        description: Private IP of the PEM server.
        required: False
      default:
        description: private_ip of the current node.
"""

EXAMPLES = """
- name: Show nodes where the PEM agent is enabled
  debug: msg="{{ lookup('pem_agent') }}"
"""

RETURN = """
_value:
  description:
    - List of Postgres nodes
  type: list
  elements:
    - dict: node_type, hostname, ansible_host (public IP address), private_ip
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        nodes = []
        if len(variables['groups']['pemserver']) == 0:
            return nodes

        myvars = getattr(self._templar, '_available_variables', {})
        # Inventory hostname
        ihn = variables['inventory_hostname']

        # If no terms, we'll used the current private IP
        if len(terms) == 0:
            pemsrv_private_ip = myvars['hostvars'][ihn]['private_ip']
        else:
            pemsrv_private_ip = terms[0]

        # Lookup for pem servers with a matching private_ip
        for node_type in ['primary', 'standby']:
            if node_type not in variables['groups']:
                continue
            for host in variables['groups'][node_type]:
                hv = myvars['hostvars'][host]

                if hv['pem_server_private_ip'] != pemsrv_private_ip:
                    continue

                nodes.append(
                    dict(
                        node_type=node_type,
                        ansible_host=hv['ansible_host'],
                        hostname=hv.get('hostname', hv['ansible_hostname']),
                        private_ip=hv['private_ip'],
                        inventory_hostname=hv['inventory_hostname']
                    )
                )
        return nodes
