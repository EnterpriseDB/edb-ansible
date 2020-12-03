#!/usr/bin/env python
# coding: utf-8

class FilterModule(object):
    def filters(self):
        return {'sort_servers': self.sort_servers}

    def sort_servers(self, servers):
        """
        Sorting function for servers dictionnary.

        Returned object is a list of dict.

        Sorting algorithm:
          1. pemserver node first
          2. all other types of node excluding primary and standby nodes
          3. loop through primary and standby nodes
            3.1 primary first
            3.2 standby when its upstream node has been moved
            3.3 if no server has been sorted during this loop iteration, then raise
                an error
        """
        # Sorted servers
        sorted_servers = []
        # List of server names that have been already sorted
        sorted_server_names = list()
        # List of sorted upstream nodes
        upstreams = list()
        # Primary node private ip (default upstream node)
        primary_private_ip = None
        # Current number of server to sort
        servers_length = len(servers.keys())
        # Servers length of last loop iteration
        last_servers_length = 0

        # Move pemserver first
        for k in list(servers):
            if servers[k]['node_type'] == 'pemserver':
                # Copy the server item into sorted_servers
                sorted_servers.append(
                    dict(list(servers[k].items()) + [('name', k)])
                )
                # Keep a track of the server name that has been sorted
                sorted_server_names.append(k)
                # Remove the server item from servers dict
                del(servers[k])
                break

        # Move all other types of node excepting primary and standby
        for k in list(servers):
            # Sanity check
            if k in sorted_server_names:
                raise Exception("Server %s already sorted")

            if servers[k]['node_type'] not in ['primary', 'standby']:
                sorted_servers.append(
                    dict(list(servers[k].items()) + [('name', k)])
                )
                sorted_server_names.append(k)
                del(servers[k])
                continue

        servers_length = len(servers.keys())

        while servers_length != 0:
            # At each loop iteration at least one server should have been moved
            # into sorted_servers. If this is not the case, we raise an error
            # because we are not able to handle this server item. Reasons for
            # this can be: unsupported node type or upstream_node not existing.

            for k in list(servers):
                # Sanity check
                if k in sorted_server_names:
                    raise Exception("Server %s already sorted")

                # Primary node case
                if servers[k]['node_type'] == 'primary':
                    sorted_servers.append(
                        dict(list(servers[k].items()) + [('name', k)])
                    )
                    sorted_server_names.append(k)
                    upstreams.append(servers[k]['private_ip'])
                    # Will be the default upstream_node if not set
                    primary_private_ip = servers[k]['private_ip']
                    del(servers[k])
                    continue

                # Standby node case
                if servers[k]['node_type'] == 'standby':
                    upstream_node = servers[k].get('upstream_node_private_ip',
                                                   primary_private_ip)
                    if upstream_node not in upstreams:
                        # Upstream node not yet sorted in this loop iteration,
                        # so, we will try again at the next iteration.
                        continue

                    sorted_servers.append(
                        dict(list(servers[k].items()) + [('name', k)])
                    )
                    sorted_server_names.append(k)
                    upstreams.append(servers[k]['private_ip'])
                    del(servers[k])
                    continue

            # Case when a server has not been sorted in this loop iteration.
            if servers_length == len(servers.keys()):
                raise Exception("Error with servers %s" % servers.keys())

            servers_length = len(servers.keys())
        return sorted_servers
