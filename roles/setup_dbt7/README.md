# setup_dbt7

This role is for installing DBT-7.

## Requirements

Following are the requirements of this role.
  1. Ansible

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt7_version***

  These playbooks can install any version of the DBT-7 AppImage that is
  packaged from GitHub.  See the following link for available versions:
  https://github.com/osdldbt/dbt7/releases

  * ***have_tpcdsfile***

  This is a boolean used for CI purposes where we cannot redistribute TPC code
  thus the CI system will not attempt to run the tasks specific for setting up
  the TPC code.

  * ***tpcdsfile***

  This is the full path to the TPC-DS Tools zip file that must be downloaded by
  you, the user, per TPC EULA agreement.  The TPC-DS Tools can be requested at:
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
        pgsql1.dbt7.internal:
          ansible_host: 10.1.1.3
          private_ip: 10.1.1.3
          dbt7: true
```

### Playbook file content

Content of the `inventory.yml` file:

Below is an example of how to include the `setup_dbt7` role:

```yaml
---
- hosts: all
  name: Postgres deployment playbook for DBT-7
  become: yes
  gather_facts: yes
  any_errors_fatal: True
  max_fail_percentage: 0

  collections:
    - edb_devops.edb_postgres

  roles:
    - role: setup_dbt7
      when: "'setup_dbt7' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

## Playbook execution examples

```bash
# To deploy community Postgres with the user centos
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
