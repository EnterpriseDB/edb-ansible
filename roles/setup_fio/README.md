# setup_fio

This role is for installing fio.

## Requirements

Following are the requirements of this role.
  1. Ansible

## Role variables

None

## Dependencies

This role depends on the `install_from_source` role.

The playbook using this rule is resposnible for make sure a C compiler and make
utility is installed.

## Example Playbook

```yaml
---
- hosts: all
  name: install fio
  become: true
  gather_facts: true

  collections:
    - edb_devops.edb_postgres

  roles:
    - setup_fio
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
