# setup_dbt2_driver

This role is for setting up a server for the
[DBT-2](https://www.github.com/osdldbt/dbt2) terminal emulators (a.k.a. the
driver) transaction manager.

This is required in a 3-tier or 2-tier client-server configurations.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository
     on the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt2_version***

  These playbooks can install any version of DBT-2 that is packaged into an AppImage from GitHub.
  See the following link for available versions:
  https://github.com/osdldbt/dbt2/releases

  * ***dbttools_version***

  These playbooks can install any version of DBT Tools that is packaged from
  GitHub but specific versions may be required depending on the version of DBT-2
  used.  Unless you have a specific reason to install a specific version, you
  will generally want to use the latest available versions.  See the following
  link for available versions:
  https://github.com/osdldbt/dbttools-packaging/releases

  * ***dbt2_path***

  This is the location where the DBT-2 AppImage will be installed.
  For ease of use, try to set this location within a directory along the executable `PATH`.
  Unless necessary, there shouldn't be any reason to change this default.

  * ***pg_owner***

  This is used to ensure the operating system user to use for running the DBT-2
  client is created.  For ease of autoamtion, this should be the same user that
  is defined for the `setup_dbt2` role.  A different default is set depending
  on which `vars` file is inherited, which is based on the PostgreSQL
  distribution selected.

These variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_dbt2_driver` role in your Playbook*.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
all:
  children:
    dbt2_driver:
      hosts:
        dbt2_driver.dbt2.internal:
          ansible_host: 10.1.1.19
          private_ip: 10.1.1.19
```

### Playbook file content

Content of the `inventory.yml` file:

Below is an example of how to include the `setup_dbt2_driver` role:

```yaml
---
- hosts: all
  name: Postgres deployment playbook for DBT-2 terminal emulator configuration.
  become: yes
  gather_facts: yes
  any_errors_fatal: True
  max_fail_percentage: 0

  collections:
    - edb_devops.edb_postgres

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_dbt2_driver
      when: "'setup_dbt2_driver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

## Playbook execution examples

```bash
# To deploy community Postgres version 13 with the user centos
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="pg_version=13 pg_type=PG"
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
