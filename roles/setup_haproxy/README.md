# setup_haproxy

This role is for installing and configuring HAProxy. HAProxy is a load balancer
for PostgreSQL.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

### `haproxy_port`

Which port to listen on. Applies to both TCP and Unix sockets. Default: `5000`

Example:
```yaml
haproxy_port: 5000
```

### `haproxy_listen_address`

Specifies a list of addresses where to listen for TCP connections. You may also
use `*` meaning “listen on all addresses”. Addresses can be specified
numerically (IPv4/IPv6) or by name. Default: `*`

Example:
```yaml
haproxy_listen_address: "*"
```

### `haproxy_global_maxconn`

The maxconn value that will be set in the global HAProxy configuration. Default: `100`

Example:
```yaml
haproxy_global_maxconn: "300"
```

### `haproxy_read_only_lb`

If set to `true`, HAProxy will configure a backend to route read-only connections to replicas.
Default: `false`

Example:
```yaml
haproxy_read_only_lb: true
```

### `haproxy_replica_port`

If `haproxy_read_only_lb: true`, the port HAProxy will listen to for read-only connections.
Default: `5001`

Example:
```yaml
haproxy_replica_port: 5001
```

### `patroni_rest_api_port`

The port of the REST API of the patroni cluster.
Default: `8008`

Example:
```yaml
patroni_rest_api_port: 8008
```


## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Hosts file content

HAProxy can be configured on any most node types. To configure HAProxy on a host,
set `haproxy_configure` to `true`. If you would like a host to be included as a backend server
to HAProxy, set `haproxy: true` and include the `proxy_location` of the proxy server the node
is a part of. 

In this example, HAProxy is being configured alongside PgBouncer for a Patroni cluster.

Content of the `inventory.yml` file:
```yaml
---
all:
  children:
    pgbouncer:
      hosts:
        proxy1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          haproxy: true
          proxy_location: 'zone_1'
          haproxy_configure: true
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          haproxy: true
          proxy_location: 'zone_1'
          etcd: true
          etcd_cluster_name: 'patroni-etcd'
```