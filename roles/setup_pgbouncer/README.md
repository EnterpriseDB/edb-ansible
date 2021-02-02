# setup_pgbouncer

This role is for installing and configuring PgBouncer. PgBouncer is a
lightweight connection pooler for PostgreSQL.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

### `pgbouncer_listen_port`

Which port to listen on. Applies to both TCP and Unix sockets. Default: `6432`

Example:
```yaml
pgbouncer_listen_port: 6432
```

### `pgbouncer_listen_addr`

Specifies a list of addresses where to listen for TCP connections. You may also
use `*` meaning “listen on all addresses”. Addresses can be specified
numerically (IPv4/IPv6) or by name. Default: `*`

Example:
```yaml
pgbouncer_listen_addr: "*"
```

### `pgbouncer_user`

System user account that runs PgBouncer process and owns its configuration
files. Default: `pgbouncer`

Example:
```yaml
pgbouncer_user: "pgbouncer"
```

### `pgbouncer_group`

System group that PgBouncer system user is part of. Default: `pgbouncer`

Example:
```yaml
pgbouncer_group: "pgbouncer"
```

### `pgbouncer_default_pool_size`

How many server connections to allow per user/database pair. Can be overridden
in the per-database configuration. Default: `20`

Example:
```yaml
pgbouncer_default_pool_size: 20
```

### `pgbouncer_max_client_conn`

Maximum number of client connections allowed. Default: `100`

Example:
```yaml
pgbouncer_max_client_conn: 100
```

### `pgbouncer_fd_limit`

File descriptor limits. Default: `2048`

Example:
```yaml
pgbouncer_fd_limit: 2048
```

### `pgbouncer_pool_mode`

Pooling mode. Could be `session`, `transaction` or `statement`.
Default: `session`

Example:
```yaml
pgbouncer_pool_mode: "session"
```

### `pgbouncer_server_reset_query`

Query sent to server on connection release, before making it available to
other clients. Default: `DISCARD ALL`

Example:
```yaml
pgbouncer_server_reset_query: "DISCARD ALL"
```

### `pgbouncer_admin_users`

Comma-separated list of database users that are allowed to connect and run all
commands on the console. Default: `pgbouncer_admin`

Example:
```yaml
pgbouncer_admin_users: "pgbouncer_admin"
```

### `pgbouncer_stats_users`

Comma-separated list of database users that are allowed to connect and run
read-only queries on the console. Default: `pgbouncer_stats`

Example:
```yaml
pgbouncer_stats_users: "pgbouncer_stats"
```

### `pgbouncer_auth_type`

How to authenticate users. Could be `pam`, `hba`, `cert`, `md5`,
`scram-sha-256`, `plain`, `trust` or `any`. Default: `scram-sha-256`

Example:
```yaml
pgbouncer_auth_type: "scram-sha-256"
```

### `pgbouncer_auth_file`

The path of the file to load user names and passwords from.
Default: `/etc/pgbouncer/userlist.txt`

Example:
```yaml
pgbouncer_auth_file: "/etc/pgbouncer/userlist.txt"
```

### `pgbouncer_auth_user`

PostgreSQL user used to run the query `auth_query` in the database when the
user is not found in the authentication file.
Default: `not defined`

Example:
```yaml
pgbouncer_auth_user: "pgbouncer"
```

### `pgbouncer_auth_query`

Query to load user’s password from database. Default: `not defined`

Example:
```yaml
pgbouncer_auth_query: "SELECT usename, passwd FROM pg_shadow WHERE usename = $1"
```

### `pgbouncer_config_file`

Main configuration file path. Default: `/etc/pgbouncer/pgbouncer.ini`

Example:
```yaml
pgbouncer_config_file: "/etc/pgbouncer/pgbouncer.ini"
```

### `pgbouncer_pid_file`

PID file path. Default: `/run/pgbouncer/pgbouncer.pid`

Example:
```yaml
pgbouncer_pid_file: "/run/pgbouncer/pgbouncer.pid"
```

### `pgbouncer_log_file`

Log file path. Default: `/var/log/pgbouncer/pgbouncer.log`

Example:
```yaml
pgbouncer_log_file: "/var/log/pgbouncer/pgbouncer.log"
```

### `pgbouncer_syslog`

Toggles syslog on/off. Default: `0`

Example:
```yaml
pgbouncer_syslog: 0
```

### `pgbouncer_syslog_ident`

Under what name to send logs to syslog. Default: `pgbouncer`

Example:
```yaml
pgbouncer_syslog_ident: "pgbouncer"
```

### `pgbouncer_databases_file`

Configuration file path that contains databases (connection pools)
configuration.
Default: `/etc/pgbouncer/databases.ini`

Example:
```yaml
pgbouncer_databases_file: "/etc/pgbouncer/databases.ini"
```

### `pgbouncer_systemd_unit_file`

Systemd unit configuration file path.
Default: `/etc/systemd/system/pgbouncer.service.d/pgbouncer.conf`

Example:
```yaml
pgbouncer_systemd_unit_file: "/etc/systemd/system/pgbouncer.service.d/pgbouncer.conf"
```

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Hosts file content

To deploy PgBouncer as a standalone application on a dedicated host,
`node_type` should be set up to `pgbouncer`. When deploying PgBouncer alongside
a Postgres instance, the key `pgbouncer` should be set up to `true`.

Content of the `inventory.yml` file:
```yaml
---
all:
  children:
    # PgBouncer pooler instance on a dedicated host
    pgbouncer:
      hosts:
        pooler1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Another PgBouncer pooler instance located on the PG host
          pgbouncer: true
```

### How to include the `setup_pgbouncer` role in your Playbook

Below is an example of how to include the `setup_pgbouncer` role:
```yaml
---
- hosts: pgbouncer,primary,standby
  name: Setup PgBouncer connection pooler
  become: true
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"

  roles:
    - role: setup_pgbouncer
      # Ensure to execute this role only on hosts from the pgbouncer group, or,
      # from the primary and standby groups having the 'pgbouncer' inventory
      # host var is set to true.
      when: "'setup_pgbouncer' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_pgbouncer/defaults/main.yml](./defaults/main.yml)

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
