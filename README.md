# PG Ansible

[![Version on Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=ansible-galalxy&prefix=v&url=https://galaxy.ansible.com/api/v2/collections/tmax_opensql/postgres/&query=latest_version.version)](https://galaxy.ansible.com/tmax_opensql/postgres)

This repository is for hosting an Ansible Galaxy Collection **hypersql_devops.postgres** which helps users easily deploy Tmax OpenSQL package for PostgreSQL.

_The ansible playbook must be executed under an account that has full
privileges._

The following table describes the roles included in **tmax_opensql.postgres** collection.

| Role name                                                        | Description                                                                                                                                                                                            |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [autotuning](roles/autotuning/README.md)                         | The autotuning role configures the system and Postgres instances for optimal performances. Most of the configuration values are calculated automatically from available resources found on the system. |
| [init_dbserver](roles/init_dbserver/README.md)                   | Initialize the PostgreSQL cluster (data) directory.                                                                                                                                                    |
| [install_dbserver](roles/install_dbserver/README.md)             | Install PostgreSQL database server packages.                                                                                                                                                           |
| [manage_extension](roles/manage_extension/README.md)               | Manage PostgreSQL Extension Packages.                                                                                                                                                    |
| [manage_dbserver](roles/manage_dbserver/README.md)               | Manage PostgreSQL clusters and covers common tasks.                                                                                                                                                    |
| [manage_pgbouncer](roles/manage_pgbouncer/README.md)             | Manage PgBouncer pools list and users.                                                                                                                                                                 |
| [manage_pgpool2](roles/manage_pgpool2/README.md)                 | Manage Pgpool-II settings and users.                                                                                                                                                                   |
| [setup_barman](roles/setup_barman/README.md)                     | Set up PostgreSQL backups with Barman.                                                                                                                                                                 |
| [setup_barmanserver](roles/setup_barmanserver/README.md)         | Set up Barman (Postgres backup) server.                                                                                                                                                                |
| [setup_pgbackrest](roles/setup_pgbackrest/README.md)             | Set up PostgreSQL backups with pgBackRest.                                                                                                                                                             |
| [setup_pgbackrestserver](roles/setup_pgbackrestserver/README.md) | Set up pgBackRest server for Postgres backups and recovery.                                                                                                                                            |
| [setup_pgbouncer](roles/setup_pgbouncer/README.md)               | Set up PgBouncer connection pooler.                                                                                                                                                                    |
| [setup_pgpool2](roles/setup_pgpool2/README.md)                   | Set up Pgpool-II connection pooler/load balancer.                                                                                                                                                      |
| [setup_replication](roles/setup_replication/README.md)           | Set up the data replication (synchronous/asynchronous).                                                                                                                                                |
| [setup_repmgr](roles/setup_repmgr/README.md)                     | Set up Repmgr for PostgreSQL HA cluster.                                                                                                                                                               |
| [setup_repo](roles/setup_repo/README.md)                         | Set up the PostgreSQL Community and EPEL repositories.                                                                                                                                                 |

## Pre-Requisites

For correctly installed and configuration of the cluster following are requirements:

1. Ansible (on the machine on which playbook will be executed).
2. Operating system privileged user (user with sudo privilege) on all the
   servers/virtual machines.
3. Machines for the Postgres cluster should have at least 2 CPUs and
   4 GB of RAM
4. The machine utilized for deploying with ansible can be a minimal instance

## Installation

To install Ansible: **[Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)**

**tmax_opensql.postgres** can be installed in the following approaches:

### Installing from Ansible Galaxy

Use the command below to install **tmax_opensql.postgres**:

```bash
ansible-galaxy collection install tmax_opensql.postgres --force
```

This approach automatically makes the **tmax_opensql.postgres** collection available to
your playbooks.

A message indicating where the collection is installed will be displayed by
ansible-galaxy. The collection code should be automatically made readily
available for you.

By default the location of your installed collection is:
`~/.ansible/collections/ansible_collections`

### Cloning the source code from the repository GitHub

Use the command below to install **tmax_opensql.postgres**:

```bash
git clone https://github.com/tmaxopensql/pg-ansible.git
cd pg-ansible
make install
```

This approach automatically makes the **tmax_opensql.postgres** collection available to
your playbooks.

A message indicating where the collection is installed will be displayed by
ansible-galaxy. The collection code should be automatically made readily
available for you.

By default the location of your installed collection is:
`~/.ansible/collections/ansible_collections`

## Example of inventory file

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: 110.0.0.1
          private_ip: 10.0.0.1
    standby:
      hosts:
        standby1:
          ansible_host: 110.0.0.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
        standby2:
          ansible_host: 110.0.0.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
```

Note: don't forget to replace IP addresses.

## How to include the roles in your Playbook

Below is an example of how to include all the roles for a deployment in a
playbook:

```yaml
---
- hosts: all
  name: Postgres deployment playbook
  become: yes
  gather_facts: yes

  collections:
    - tmax_opensql.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"
        disable_logging: false

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: install_dbserver
      when: "'install_dbserver' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: init_dbserver
      when: "'init_dbserver' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: manage_extension
      when: "'manage_extension' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_replication
      when: "'setup_replication' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_pgpool2
      when: "'setup_pgpool2' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: manage_pgpool2
      when: "'manage_pgpool2' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: manage_dbserver
      when: "'manage_dbserver' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_pgbackrest
      when: "'setup_pgbackrest' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_pgbackrestserver
      when: "'setup_pgbackrestserver' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_pgbouncer
      when: "'setup_pgbouncer' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: manage_pgbouncer
      when: "'manage_pgbouncer' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_barmanserver
      when: "'setup_barmanserver' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: setup_barman
      when: "'setup_barman' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
    - role: autotuning
      when: "'autotuning' in lookup('tmax_opensql.postgres.supported_roles', wantlist=True)"
```

You can customize the above example to install Tmax OpenSQL Package by selecting which roles you would like to execute.

## Default user and passwords

The following will occur should a password not be provided for the following
accounts:

- `pg_superuser`
- `pg_replication_user`

**Note:**

- The `~/.pgpassfile` folder and contained files are secured by assigning the
  permissions to `user` executing the playbook.
- The naming convention for the password file is: `<username>_pass`

## Playbook examples

Examples of utilizing the playbooks for installing Tmax OpenSQL Package are provided and located within the `playbook-examples` directory.

## SSH port configuration

When using non standard SSH port (different from 22), the port value must be
set in two places:

- in the inventory file, for each host, with the host var. `ansible_port`
- in the playbook or variable file with the variable `ssh_port`

## Playbook execution examples

```bash
# To deploy community Postgres version 14.6
ansible-playbook playbook.yml \
  -i inventory.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_version=14.6 pg_type=PG"
```

## Database engines supported

### Supported OS
- CentOS7
- CentOS8

### Supported PostgreSQL Version
- 14.0 - 14.6

## License

BSD

## Author information

Authors:

- [Sung Woo Chang](https://github.com/dbxpert)
- [Sang Myeung Lee](https://github.com/sungmu1)
