# setup_dbt3

This role is for installing DBT-3.



## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt3_pgdata***

  This variable is to be used to specify a custom PGDATA directory that DBT-3
  will use separately from the default PGDATA that may be used in other
  playbooks.  Thus do not set this to a directory that may be used elsewhere.
  You are not likely to use this unless you are testing specific source based
  installations of PostgreSQL or doing any other highly customized testing with
  logical or physical system configurations.

  * ***dbt3_version***

  These playbooks can install any version of DBT-3 that is packaged from GitHub.
  See the following link for available versions:
  https://github.com/osdldbt/dbt3-packaging/releases

  * ***have_tpcfile***

  The is a boolean use for CI purposes where we cannot redistribute TPC code
  thus the CI system will not attempt to run the tasks specific for setting up
  the TPC code.

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13 and 14

  * ***tpcfile***

  This is the full path to the TPC-H Tools zip file that must be downloaded by
  the you, the user, per TPC EULA agreement.  The TPC-H Tools can be requested
  at:
  https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp

These variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_dbt3` role in your Playbook*.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
all:
  children:
    primary:
      hosts:
        pgsql1.dbt3.internal:
          ansible_host: 10.1.1.3
          private_ip: 10.1.1.3
          dbt3: true
```

### Playbook file content

Content of the `inventory.yml` file:

Below is an example of how to include the `setup_dbt3` role:

```yaml
---
- hosts: all
  name: Postgres deployment playbook for DBT-3
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
    - role: setup_dbt3
      when: "'setup_dbt3' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
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
