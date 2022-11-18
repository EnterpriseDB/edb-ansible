# autotuning

The autotuning role configures the system and Postgres instances for optimal
performances. Most of the configuration values are calculated automatically
from available resources found on the system.

## Requirements

Following are the dependencies and requirement of this role.
  1. Ansible

## Role Variables

When executing the role via ansible these are the required variables:

  * pg_version (available: 11, 12, 13, 14)
  * pg_type (available: PG, HyperSQL)

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `autotuning` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/autotuning/defaults/main.yml](./defaults/main.yml)
  * [roles/autotuning/vars/main.yml](./vars/main.yml)

### `tuned_profile`

This is the `tuned` profile name used for configuring the system. Default: `postgres`

Example:
```yaml
tuned_profile: "postgres"
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
- hosts: primary,standby
  name: Apply system and Postgres recommanded performance tuning
  become: true
  gather_facts: yes

  collections:
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_type: "PG"
        pg_version: 14
        ssd_disk: yes

  roles:
    - role: autotuning
```
## License

BSD

## Author information
Author:
  * [Sung Woo Chang](https://github.com/dbxpert)

Original Author:
  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
