# setup_dbt2

this role is for setting up [dbt-2](https://www.github.com/osdldbt/dbt2) related
components on the database server.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. An already initialized database cluster, or the roles required to do so within the same playbook.
  3. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository
     on the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***dbt2_version***

  These playbooks can install any version of DBT-2 that is packaged into an AppImage from GitHub.
  See the following link for available versions:
  https://github.com/osdldbt/dbt2/releases

  * ***dbt2_path***

  This is the location where the DBT-2 AppImage will be installed.
  For ease of use, try to set this location within a directory along the executable `PATH`.
  Unless necessary, there shouldn't be any reason to change this default.

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13, 14 and 15.

  * ***pg_dbt2_dbname***

  This is the database name to use specifically for the test.


These variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_dbt2` role in your Playbook*.

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
          dbt2: true
```

### Playbook file content

Content of the `inventory.yml` file:

Below is an example of how to include the `setup_dbt2` role:

```yaml
---
- hosts: all
  name: Postgres deployment playbook for DBT-2 database server configuration.
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
    - role: setup_dbt2
      when: "'setup_dbt2' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: tuning
      when: "'tuning' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
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
