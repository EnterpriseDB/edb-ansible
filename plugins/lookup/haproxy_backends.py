from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: haproxy_backends
    author: Hannah Stoik
    short_description: Lookup function for haproxy backend nodes
    description:
      - "Retrieves the haproxy backend nodes list"
    options:
      _terms:
        description: haproxy location variable.
        required: False
      default:
        description: proxy_location of local node.
"""

EXAMPLES = """
- name: Show all members of the haproxy location
  debug: msg="{{ lookup('haproxy_backends') }}"

- name: Show all members of the haproxy backend cluster located in the named 
  debug: msg="{{ lookup('haproxy_backends', 'zone_1') }}"
"""

RETURN = """
_value:
  description:
    - List of haproxy backend nodes
  type: list
  elements: dict
"""


from ansible.plugins.lookup import LookupBase
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        # define empty list of haproxy_backends
        haproxy_backends = []

        myvars = getattr(self._templar, '_available_variables', {})
        inventory_hostname = variables['inventory_hostname']

        # if no terms, we will use current proxy_location
        if len(terms) == 0:
            if 'proxy_location' not in myvars['hostvars'][inventory_hostname]:
                # proxy location not set, return None
                return []
            proxy_location = myvars['hostvars'][inventory_hostname]['proxy_location']
        else:
            proxy_location = terms[0]

        # Lookup for servers with the same proxy_location
        for group in ['primary', 'standby', 'pemserver', 'pgbouncer', 'pgpool2',
                      'barmanserver', 'witness', 'proxy', 'pgbackrestserver']:
            if group not in variables['groups']:
                continue

            for host in variables['groups'][group]:
                hostvars = myvars['hostvars'][host]
                if 'haproxy' not in hostvars:
                    continue
                if hostvars.get('haproxy'):
                    if 'proxy_location' not in hostvars:
                        continue

                    if hostvars.get('proxy_location') != proxy_location:
                        continue

                    backend_node = dict(
                        ansible_host=hostvars.get('ansible_host'),
                        inventory_hostname=hostvars['inventory_hostname'],
                        hostname=hostvars.get('hostname', hostvars['ansible_hostname']),
                        proxy_location=hostvars.get('proxy_location', hostvars['proxy_location']),
                        private_ip=hostvars['private_ip'],
                        node_type=group,
                        haproxy_configure=hostvars.get('haproxy_configure', False)
                    )

                    haproxy_backends.append(backend_node)

        return haproxy_backends
