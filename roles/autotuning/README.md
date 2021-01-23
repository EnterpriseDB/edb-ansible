# autotuning

The autotuning role configures the system and Postgres instances for optimal
performances. Most of the configuration values are calculated automatically
from available resources found on the system.

## Requirements

Following are the dependencies and requirement of this role.
  1. Ansible

## Role Variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `autotuning` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/autotuning/defaults/main.yml](./defaults/main.yml)
  * [roles/autotuning/vars/EPAS.yml](./vars/EPAS.yml)
  * [roles/autotuning/vars/PG.yml](./vars/PG.yml)


### `tuned_profile`

This is the `tuned` profile name used for configuring the system. Default: `edb`

Example:
```yaml
tuned_profile: "edb"
```

### `tuned_configuration_dir`

`tuned` configuration directory path. Default: `/etc/tuned`

Example:
```yaml
tuned_configuration_dir: "/etc/tuned"
```

### `ssd_disk`

Let the role knows if the system uses SSD disk based storage. Default: `no`

Example:
```yaml
ssd_disk: yes
```

## Dependencies

This role does not have any dependencies, but a Postgres instance should have
been deployed beforehand with the `init_dbserver` or `setup_replication` roles.

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
```

### How to include the `autotuning` role in your Playbook

Below is an example of how to include the `autotuning` role:
```yaml
---
- hosts: pemserver,primary,standby
  name: Apply system and Postgres recommanded performance tuning
  become: true
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_type: "PG"
        pg_version: 13

        ssd_disk: yes

  roles:
    - role: autotuning
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/autotuning/defaults/main.yml](./defaults/main.yml)
  * [roles/autotuning/vars/EPAS.yml](./vars/EPAS.yml)
  * [roles/autotuning/vars/PG.yml](./vars/PG.yml)

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
