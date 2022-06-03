# setup_dbt2

This role is for installing DBT-2.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository
     on the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt2_version***

  These playbooks can install any version of DBT-2 that is packaged from GitHub.
  See the following link for available versions:
  https://github.com/osdldbt/dbt2-packaging/releases

  * ***dbttools_version***

  These playbooks can install any version of DBT Tools that is packaged from
  GitHub but specific versions may be required depending on the version of DBT-2
  used.  Unless you have a specific reason to install a specific version, you
  will generally want to use the latest avaialble versions.  See the following
  link for available versions:
  https://github.com/osdldbt/dbttools-packaging/releases

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13 and 14

  * ***pg_dbt2_dbname***

  This is the database name to use specifically for the test.


These variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_dbt2` role in your Playbook*.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file for 3-tier client-server architecture.
A 2-tier configuration can be used by removing the `dbt2_client` section:

```yaml
all:
  children:
    primary:
      hosts:
        pgsql1.dbt2.internal:
          ansible_host: 10.1.1.3
          private_ip: 10.1.1.3
          dbt2: true
    dbt2_driver:
      hosts:
        dbt2_driver1.dbt2.internal:
          ansible_host: 10.1.1.19
          private_ip: 10.1.1.19
    dbt2_client:
      hosts:
        dbt2_client.dbt2.internal:
          ansible_host: 10.1.1.11
          private_ip: 10.1.1.11
```

### Playbook file content

Content of the `inventory.yml` file:

Below is an example of how to include the `setup_dbt2` role:

```yaml
---
- hosts: all
  name: Postgres deployment playbook for 3-tier DBT-2 configuration.
  become: yes
  gather_facts: yes
  any_errors_fatal: True
  max_fail_percentage: 0

  collections:
    - edb_devops.edb_postgres

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: install_dbserver
      when: "'install_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: init_dbserver
      when: "'init_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_dbt2_driver
      when: "'setup_dbt2_driver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_dbt2_client
      when: "'setup_dbt2_client' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_dbt2
      when: "'setup_dbt2' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: autotuning
      when: "'autotuning' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
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
