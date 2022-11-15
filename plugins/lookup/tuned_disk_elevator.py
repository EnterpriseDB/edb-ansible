from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: tuned_disk_elevator 
    author: Sung Woo Chang 
    short_description: Returns the disk elevator type for TuneD 
"""

EXAMPLES = """
"""

RETURN = """
"""

from ansible.plugins.lookup import LookupBase
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
      os_family = variables.get('ansible_os_family')
      os_major_version = variables.get('ansible_distribution_major_version')

      disk_elevator_type = 'deadline'

      if os_family == 'RedHat' and os_major_version == '8'
        disk_elevator_type = 'mq-deadline'
       
      return [disk_elevator_type]
