from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pg_service
    author: Julien Tachoires
    short_description: Returns systemd service name for PostgreSQL/EPAS on RHEL
"""

EXAMPLES = """
"""

RETURN = """
"""

from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        pg_type = variables.get('pg_type', '13')
        pg_version = variables.get('pg_version', 'PG')
        pg_instance_name = variables.get('pg_instance_name', 'main')

        if pg_type == 'EPAS':
            p = 'edb-as-%s'
        elif pg_type == 'PG':
            p = 'postgresql-%s'
        if pg_instance_name != 'main':
            return [(p + '-%s') % (pg_version, pg_instance_name)]
        else:
            return [p % pg_version]
