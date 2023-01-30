from __future__ import absolute_import, division, print_function

from ansible.plugins.lookup import LookupBase

__metaclass__ = type

DOCUMENTATION = """
    name: pg_service
    author: Julien Tachoires
    short_description: Returns systemd service name for PostgreSQL
"""

EXAMPLES = """
"""

RETURN = """
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.pg_major_version = str(variables.get("pg_version")).split('.')[0]
        self.pg_instance_name = variables.get("pg_instance_name", "main")
        self.os_family = variables.get("ansible_os_family")

        pg_service_name = self.get_pg_service_name()

        return [pg_service_name]

    def get_pg_service_name(self):
        pg_service_name = ""

        if self.os_family == "RedHat":
            pg_service_name = self.get_pg_service_name_for_redhat()
        elif self.os_family == "Debian":
            pg_service_name = self.get_pg_service_name_for_debian()
        else:
            raise Exception("Unsupported OS Type")

        return pg_service_name

    def get_pg_service_name_for_redhat(self):
        pg_service_name = "postgresql-%s"

        if self.pg_instance_name != "main":
            pg_service_name = (pg_service_name + "-%s") % (
                self.pg_major_version,
                self.pg_instance_name,
            )
        else:
            pg_service_name = pg_service_name % self.pg_major_version

        return pg_service_name

    def get_pg_service_name_for_debian(self):
        return "postgresql@%s-%s" % (self.pg_major_version, self.pg_instance_name)
