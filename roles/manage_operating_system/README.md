# manage_operating_system

This role is for managing operating system settings.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. An already initialized system running Linux.

## Role Variables

When executing the role via Ansible these are the applicable variables:

  * ***enable_core_dump***

    When `true`, enable operating system facilities to capture and save core
    dumps.  Default: `false`

  * ***enable_user_profiling***

    When `true`, sets relevant operating system settings such that any user and
    profile the system as well as disabling any masking of operating system
    kernel memory addresses.  Default: `false`

These variables can be assigned in the `pre_tasks` definition of the Playbook.

## Example Playbook

### Inventory file content

Content of the `inventory.yml`:

```yaml
all:
  children:
    primary:
      hosts:
        pgsql1.dbt2.internal:
          ansible_host: 10.1.1.3
          private_ip: 10.1.1.3
```

### Playbook file content

Content of the `inventory.yml` file:

```yaml
---
- hosts: all
  name: Example
  become: yes

  pre_tasks:
    - name: Initialize the user defined variables
      ansible.builtin.set_fact:
        enable_core_dump: true
        enable_user_profiling: true

  collections:
    - edb_devops.edb_postgres

  roles:
    - role: manage_operating_system
```

## Playbook execution examples

```bash
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="enable_user_profiling=true enable_core_dump=true"
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
