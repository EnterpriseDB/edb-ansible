# setup_pgpool2

This role is for installing and configuring PgpoolII. PgpoolII is a
connection pooler for PostgreSQL.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_pgpool2` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_pgpool2/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgpool2/vars/PG.yml](./vars/PG.yml)
  * [roles/setup_pgpool2/vars/EPAS.yml](./vars/EPAS.yml)

Below is the documentation of the rest of the main variables:

### `pgpool2_watchdog`

Enable PgpoolII High Availability capability when deploying a PgpoolII multi
nodes cluster (3, 5 etc..). Default: `false`

Example:
```yaml
pgpool2_watchdog: true
```

### `pgpool2_vip`

Thie is the virtual IP address to put on the Pgpool2 primary node when
deploying a PgpoolII multi node cluster. Watchdog feature must be enabled.
Default: empty.

Example:
```yaml
pgpool2_vip: "10.0.0.123"
```

### `pgpool2_vip_dev`

System's network device to attach the virtual IP address. Default: empty.

Example:
```yaml
pgpool2_vip_dev: "eth0"
```

### `pgpool2_load_balancing`

Enable read only queries load balancing across all the Postgres nodes.
Default: `true`.

Example:
```yaml
pgpool_load_balancing: true
```

### `pgpool2_ssl`

Enable SSL support. Default: `true`.

Example:
```yaml
pgpool2_ssl: true
```

### `pgpool2_port`

Pgpool2 listening TCP port. Default: `9999`.

Example:
```yaml
pgpool2_port: 5433
```

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pgpool2:
      hosts:
        pool1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
        pool2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
        pool3:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # Private IP address of the PG primary node
          primary_private_ip: xxx.xxx.xxx.xxx
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

### How to include the `setup_pgpool2` role in your Playbook

Below is an example of how to include the `setup_pgpool2` role:
```yaml
---
- hosts: pgpool2
  name: Deploy PgpoolII instances
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"

        pgpool2_load_balancing: true
        pgpool2_watchdog: true
        pgpool2_vip: "10.0.0.123"
        pgpool2_vip_dev: "eth0"
        pgpool2_port: 5433

  roles:
    - setup_pgpool2
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_pgpool2/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgpool2/vars/EPAS.yml](./vars/EPAS.yml)
  * [roles/setup_pgpool2/vars/PG.yml](./vars/PG.yml)

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
