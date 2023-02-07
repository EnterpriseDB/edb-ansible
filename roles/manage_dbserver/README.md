# manage_dbserver

`manage_dbserver` role is for managing the database cluster. It makes the
managing of the database cluster by giving key tasks. In all the roles, we have
used the tasks given in the this role.

## Requirements

Following are the dependencies and requirement of this role.

1. Ansible
2. `community.general` Ansible Module - Utilized when creating aditional
   users during a Postgres Install

## Role variables

This role requires the following variables to be defined:

- pg_type (available: PG, HyperSQL)
- pg_version (available: 14)

This role allows users to pass following variables which helps managing day to
day tasks:

### `pg_postgres_conf_params`

Using this parameters user can set the database parameters.

Example:

```yaml
pg_postgres_conf_params:
  - name: listen_addresses
    value: "*"
```

### `pg_hba_ip_addresses`

With this parameter, user can manage HBA (Host Based Authentication) entries.

```yaml
pg_hba_ip_addresses:
  - contype: "host"
    users: "all"
    databases: "all"
    method: "scram-sha-256"
    source: "127.0.0.1/32"
    state: present
```

### `pg_slots`

Replication slots management.

```yaml
pg_slots:
  - name: "physical_slot"
    slot_type: "physical"
    state: present
  - name: "logical_slot"
    slot_type: "logical"
    output_plugin: "test_decoding"
    state: present
    database: "postgres"
```

### `pg_extensions`

Postgres extensions management.

```yaml
pg_extensions:
  - name: "postgis"
    database: "postgres"
    state: present
```

### `pg_grant_privileges`

Grant privileges management.

```yaml
pg_grant_privileges:
  - roles: "postgres_role"
    database: "postgres"
    privileges: execute
    schema: pg_catalog
    objects: pg_current_wal_lsn(),pg_last_wal_replay_lsn(),pg_wal_replay_resume(),pg_wal_replay_pause()
    type: function
```

### `pg_grant_roles`

Grant roles management.

```yaml
pg_grant_roles:
  - role: pg_monitor
    user: postgres_user
```

### `pg_sql_scripts`

SQL script execution.

```yaml
pg_sql_scripts:
  - file_path: "/usr/postgres/sample.sql"
    db: postgres
```

### `pg_copy_files`

Copy file on remote host.

```yaml
pg_copy_files:
  - file: "./test.sh"
    remote_file: "/var/lib/postgres/test.sh"
    owner: postgres
    group: postgres
    mode: 0700
```

### `pg_query`

Execute a query on a database.

```yaml
pg_query:
  - query: "Update test set a=b"
    db: postgres
```

### `pg_pgpass_values`

`.pgpass` file content management.

```yaml
pg_pgpass_values:
  - host: "127.0.0.1"
    database: postgres
    user: postgres_user
    password: <password>
    state: present
```

### `pg_databases`

Databases management.

```yaml
pg_databases:
  - name: another_postgres
    owner: postgres
    encoding: UTF-8
```

### `pg_tablespaces`

Tablesapces management.

```yaml
pg_tablespaces:
  - name: index_tablespace
    owner: postgres
    location: "/data/index_tablespace"
    state: present
```

## Dependencies

The `manage_dbserver` role does depend on the following roles:

- `community.general`

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### How to include the `manage_dbserver` role in your Playbook

Below is an example of how to include the `manage_dbserver` role:

```yaml
---
- hosts: primary,standby
  name: Manage Postgres server
  become: true
  gather_facts: true

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

        pg_postgres_conf_params:
          - name: listen_addresses
            value: "*"

        pg_hba_ip_addresses:
          - contype: "host"
            users: "all"
            databases: "all"
            method: "scram-sha-256"
            source: "127.0.0.1/32"
            state: present

        pg_slots:
          - name: "physcial_slot"
            slot_type: "physical"
            state: present
          - name: "logical_slot"
            slot_type: "logical"
            output_plugin: "test_decoding"
            state: present
            database: "postgres"

  roles:
    - manage_dbserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/manage_dbserver/defaults/main.yml](./defaults/main.yml)
- [roles/manage_dbserver/vars/main.yml](./vars/main.yml)
- [roles/manage_dbserver/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
- [roles/manage_dbserver/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Database engines supported

### Supported OS
- CentOS7
- CentOS8

### Supported PostgreSQL Version
- 14.0 - 14.6

## License

BSD

## Author information

Author:

- [Sung Woo Chang](https://github.com/dbxpert)

Original Author:

- Doug Ortiz
- Julien Tachoires
- Vibhor Kumar
- EDB Postgres
- DevOps
