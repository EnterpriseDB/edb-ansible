from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: pg_conf_params_boolean
    author: Hannah Stoik
    short_description: Returns pg_postgres_conf_params value(s) as on/off if boolean
    description:
      - "Returns pg_postgres_conf_params value(s) as on/off if boolean"
    options:
      _terms:
        description: pg_postgres_conf_params, a list of postgres parameters and values.
        required: True
      default:
        description: pg_postgres_conf_params
"""

EXAMPLES = """
- name: Show postgresql.conf values of parameters in pg_postgres_conf_params if they are boolean
  debug: msg="{{ lookup('pg_conf_params_boolean', pg_postgres_conf_params) }}"
"""

RETURN = """
_value:
  description:
    - List of postgres params 
  type: list
  elements:
    - dict: name, value, original_value (if boolean)
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

def get_pg_on_off(value):
    if value.lower() in ['on', 'true', 'yes']:
        return 'on'
    elif value.lower() in ['off', 'false', 'no']:
        return 'off'


def is_pg_bool(param_dict):
    if str(param_dict["value"]).lower() in ['on', 'off', 'true', 'false', 'yes', 'no']:
        return True
    else:
        return False


def get_dict_vals(parameter):
    if is_pg_bool(parameter):
        new_parameter = dict(
            name=str(parameter["name"]),
            value=get_pg_on_off(str(parameter["value"])),
            original_value=str(parameter["value"])
        )
        return new_parameter
    else:
        return parameter


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if len(terms) == 0:
            return []
        elif len(terms) > 1:
            raise AnsibleError(
                "Must input list of postgres configuration parameters."
                "Check lookup function input values."
            )

        if isinstance(terms[0], list):
            bool_conf_params = list(map(get_dict_vals, terms[0]))
            return bool_conf_params
        else:
            raise AnsibleError(
                "TypeError: Must input a list."
            )
