# manage_pgbouncer_users

This role is for managing PgBouncer users.
PgBouncer is a lightweight connection pooler for PostgreSQL.

## Requirements

Following are the dependencies and requirement of this role.
  1. Ansible
  2. `edb_devops.postgres` -> `setup_pgbouncer` role for setting up PgBouncer
     on the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***os***

    Operating Systems supported are: CentOS7, CentOS8, RHEL7 and RHEL8

The rest of the variables can be configured and are available in the:

  * [roles/manage_pgbouncer_users/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the variables:

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

### `pgbouncer_pid_file`

PID file path. Default: `/run/pgbouncer/pgbouncer.pid`

Example:
```yaml
pgbouncer_pid_file: "/run/pgbouncer/pgbouncer.pid"
```

### `pgbouncer_auth_file`

The path of the file to load user names and passwords from.
Default: `/etc/pgbouncer/userlist.txt`

Example:
```yaml
pgbouncer_auth_file: "/etc/pgbouncer/userlist.txt"
```

### `pgbouncer_auth_user_list`

List of user names and passwords residing in the authentication file.
Default: `[]`

Example:
```yaml
pgbouncer_auth_user_list:
  - username: "my_user"
    password: "SCRAM-SHA-256$4096:xxx...xxx"
  - username: "pgbouncer_admin"
    password: "xxxxxx"
  - username: "pgbouncer_stats"
    password: "xxxxxx"
```

## Dependencies

This role does not have any dependencies, but a PgBouncer instance should have
been deployed beforehand with the `setup_pgbouncer` role.

## Example Playbook

### Hosts file content

To manage PgBouncer as a standalone application on a dedicated host,
`node_type` should be set up to `pgbouncer`. When managing PgBouncer alongside
a Postgres instance, the key `pgbouncer` should be set up to `true`.

`hosts.yml` content example:
```yaml
---
servers:
  pooler:
    node_type: pgbouncer
    public_ip: xxx.xxx.xxx.xxx
  main:
    node_type:  primary
    public_ip: xxx.xxx.xxx.xxx
    private_ip: xxx.xxx.xxx.xxx
    pgbouncer: true
```

### How to include the `manage_pgbouncer_users` role in your Playbook

Below is an example of how to include the `manage_pgbouncer_users` role:
```yaml
---
- hosts: localhost
  name: Manage PgBouncer users
  become: true
  gather_facts: no

  collections:
    - edb_devops.edb_postgres

  vars_files:
    - hosts.yml

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        os: "CentOS8"
        pgbouncer_auth_user_list:
          - username: "my_user"
            password: "SCRAM-SHA-256$4096:xxx...xxx"
          - username: "pgbouncer_admin"
            password: "xxxxxx"
          - username: "pgbouncer_stats"
            password: "xxxxxx"

  roles:
    - manage_pgbouncer_users
```

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * julien.tachoires@enterprisedb.com www.enterprisedb.com
