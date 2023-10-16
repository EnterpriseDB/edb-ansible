# setup_dbt3

This role is for installing DBT-3.

## Requirements

Following are the requirements of this role.
  1. Ansible

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt3_version***

  These playbooks can install any version of the DBT-3 AppImage that is
  packaged from GitHub.  See the following link for available versions:
  https://github.com/osdldbt/dbt3/releases

  * ***have_tpcfile***

  This is a boolean used for CI purposes where we cannot redistribute TPC code
  thus the CI system will not attempt to run the tasks specific for setting up
  the TPC code.

  * ***tpcfile***

  This is the full path to the TPC-H Tools zip file that must be downloaded by
  you, the user, per TPC EULA agreement.  The TPC-H Tools can be requested at:
  https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp

These variables can be assigned in the `pre_tasks` definition of the
section.

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
    - role: setup_dbt3
      when: "'setup_dbt3' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

## Playbook execution examples

```bash
# To deploy community Postgres version 13 with the user centos
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="pg_type=PG"
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
