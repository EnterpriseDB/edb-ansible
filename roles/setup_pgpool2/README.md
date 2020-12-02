# setup_pgpool2

This role is for installing and configuring PgpoolII. PgpoolII is a
connection pooler for PostgreSQL.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***os***

    Operating Systems supported are: CentOS7, CentOS8, RHEL7 and RHEL8

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
node cluster. Default: `false`

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

### `pgpool2_configuration`

Configuration parameter values overiding default values. The default
configuration values have been defined in the `pgpool2_default_configuration`.
Please do not change values from the `pgpool2_default_configuration` variables
and please use the `pgpool2_configuration` variable. Default: `[]`

Example:
```yaml
pgpool2_configuration:
  - key: "port"
    value: 6432
```

Please refer to the `manage_pgpool2` roles' README file for more information.

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Hosts file content

To deploy PgpoolII as a standalone application on a dedicated host, `node_type`
should be set up to `pgpool2`.

`hosts.yml` content example:
```yaml
---
servers:
  pooler1:
    node_type: pgpool2
    public_ip: xxx.xxx.xxx.xxx
    private_ip: xxx.xxx.xxx.xxx
  pooler2:
    node_type: pgpool2
    public_ip: xxx.xxx.xxx.xxx
    private_ip: xxx.xxx.xxx.xxx
  main:
    node_type: primary
    public_ip: xxx.xxx.xxx.xxx
    private_ip: xxx.xxx.xxx.xxx
  standby:
    node_type: standby
    public_ip: xxx.xxx.xxx.xxx
    private_ip: xxx.xxx.xxx.xxx
```

### How to include the `setup_pgpool2` role in your Playbook

Below is an example of how to include the `setup_pgpool2` role:
```yaml
---
- hosts: localhost
  name: Setup Pgpool2 connection pooler
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
        pg_version: 13
        pg_type: "PG"

        # PgpoolII settings

        # Enable read only queries load balancing
        pgpool2_load_balancing: true
        # Enable HA
        pgpool2_watchdog: true
        pgpool2_vip: "10.0.0.123"
        pgpool2_vip_dev: "eth0"
        # Enable SSL support
        pgpool2_ssl: true
        # Change listening port to 6432
        pgpool2_configuration:
          - key: "port"
            value: 6432

  roles:
    - setup_pgpool2
```

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * julien.tachoires@enterprisedb.com www.enterprisedb.com
