from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: efm_nodes
    author: Julien Tachoires
    short_description: Lookup for EFM nodes
    description:
      - "Retrieves the EFM nodes list, based on node's private IP"
    options:
      _terms:
        description: The private IP of one member of the EFM cluster.
        required: False
      default:
        description: The private IP of the current node is used.
"""

EXAMPLES = """
- name: Show all members of the EFM cluster that the current node is part of
  debug: msg="{{ lookup('efm_nodes') }}"

- name: Show all members of the EFM cluster that the {{ primary_private_ip }} is part of
  debug: msg="{{ lookup('efm_nodes', primary_private_ip) }}"
"""

RETURN = """
_value:
  description:
    - List of Postgres nodes
  type: list
  elements: dict
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):

        efm_clusters = {}
        efm_standbys = {}
        efm_witnesses = {}
        efm_primary_map = {}

        myvars = getattr(self._templar, "_available_variables", {})

        # If no terms, we'll used the current private IP
        if len(terms) == 0:
            node_private_ip = myvars["hostvars"][variables["inventory_hostname"]][
                "private_ip"
            ]  # noqa
        else:
            node_private_ip = terms[0]

        # If no primary found in the inventory we return an empty list
        if "primary" not in variables["groups"]:
            return []

        # Initiate efm_clusters and efm_primary_map for each primary node we have
        # in the inventory.
        for host in variables["groups"]["primary"]:
            hostvars = myvars["hostvars"][host]
            private_ip = hostvars["private_ip"]

            efm_clusters[private_ip] = []
            efm_clusters[private_ip].append(
                dict(
                    node_type="primary",
                    ansible_host=hostvars["ansible_host"],
                    hostname=hostvars.get("hostname", hostvars.get("ansible_hostname")),
                    private_ip=hostvars["private_ip"],
                    upstream_node_private_ip=None,
                    replication_type=None,
                    inventory_hostname=hostvars["inventory_hostname"],
                )
            )
            efm_primary_map[private_ip] = private_ip

        # Populate efm_standbys dict if we have standby nodes in the inventory
        if "standby" in variables["groups"]:
            for host in variables["groups"]["standby"]:
                hostvars = myvars["hostvars"][host]
                efm_standbys[host] = dict(
                    node_type="standby",
                    ansible_host=hostvars["ansible_host"],
                    hostname=hostvars.get("hostname", hostvars.get("ansible_hostname")),
                    private_ip=hostvars["private_ip"],
                    upstream_node_private_ip=hostvars["upstream_node_private_ip"],
                    replication_type=hostvars.get("replication_type", "asynchronous"),
                    inventory_hostname=hostvars["inventory_hostname"],
                )

        efm_standbys_len = len(efm_standbys.keys())

        # Populate efm_witnesses dict if we have witness nodes in the inventory
        if "witness" in variables["groups"]:
            for host in variables["groups"]["witness"]:
                hostvars = myvars["hostvars"][host]
                efm_witnesses[host] = dict(
                    node_type="witness",
                    ansible_host=hostvars["ansible_host"],
                    hostname=hostvars.get("hostname", hostvars.get("ansible_hostname")),
                    private_ip=hostvars["private_ip"],
                    upstream_node_private_ip=hostvars["upstream_node_private_ip"],
                    replication_type=None,
                    inventory_hostname=hostvars["inventory_hostname"],
                )

        efm_witnesses_len = len(efm_witnesses.keys())

        # Append the standby nodes into the right efm_clusters item, based on
        # standby's upstream node.
        while efm_standbys_len != 0:

            for k in list(efm_standbys.keys()):
                sby = efm_standbys[k]

                if sby["upstream_node_private_ip"] in efm_primary_map:
                    upstream_private_ip = sby["upstream_node_private_ip"]
                    primary_private_ip = efm_primary_map[upstream_private_ip]
                    efm_primary_map[sby["private_ip"]] = primary_private_ip
                    efm_clusters[primary_private_ip].append(sby)
                    del efm_standbys[k]

            # Case when at least one host has not been handled in this loop
            # iteration.
            if efm_standbys_len == len(efm_standbys.keys()):
                raise AnsibleError(
                    "Inventory error with the following standbys nodes %s. "
                    "Upstream node is not configured or not found"
                    % [s for s in efm_standbys.keys()]
                )

            efm_standbys_len = len(efm_standbys.keys())

        # Append witness nodes into the right efm_clusters item, based on
        # witness's upstream node.
        while efm_witnesses_len != 0:

            for k in list(efm_witnesses.keys()):
                wit = efm_witnesses[k]

                if wit["upstream_node_private_ip"] in efm_primary_map:
                    upstream_private_ip = wit["upstream_node_private_ip"]
                    primary_private_ip = efm_primary_map[upstream_private_ip]
                    efm_primary_map[wit["private_ip"]] = primary_private_ip
                    efm_clusters[primary_private_ip].append(wit)
                    del efm_witnesses[k]

            # Case when at least one host has not been handled in this loop
            # iteration.
            if efm_witnesses_len == len(efm_witnesses.keys()):
                raise AnsibleError(
                    "Inventory error with the following witness nodes %s. "
                    "Upstream node is not configured or not found"
                    % [s for s in efm_witnesses.keys()]
                )

            efm_witnesses_len = len(efm_witnesses.keys())

        if node_private_ip in efm_primary_map:
            # Current node is part of one of the SR clusters found
            return efm_clusters[efm_primary_map[node_private_ip]]
        else:
            primary_private_ips = list(efm_clusters.keys())
            # If the current node is not part of any EFM cluster found, but,
            # only one EFM cluster has been found, then we return this EFM
            # cluster because there is no doubt.
            if len(primary_private_ips) == 1:
                return efm_clusters[primary_private_ips[0]]
            else:
                raise AnsibleError(
                    "Unable to find the EFM cluster topology because multiple "
                    "EFM clusters were found and this current node does not "
                    "appear to be part of any of them"
                )
