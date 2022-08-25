[![Tests status](https://github.com/EnterpriseDB/edb-ansible/workflows/edb-ansible%20testing/badge.svg)](https://github.com/EnterpriseDB/edb-ansible/actions?query=workflow%3Aedb-ansible-testing)

This is an open-source project and is not officially supported by EDB Support.
This repository is maintained and supported by the EDB GitHub members of this
repository. Please provide feedback by posting issues and contribute by
creating pull requests.

# edb_postgres

This Ansible Galaxy Collection brings reference architecture deployment
capabilites for PostgreSQL or EnterpriseDB Postgres Advanced Server.

**Not all Distribution or versions are supported on all the operating systems
available.**

**The ansible playbook must be executed under an account that has full
privileges.**


`edb-ansible` is a repository used for hosting an Ansible Collection that
currently supports the following ansible roles:

| Role name                                                    | Description |
| -------------------------------------------------------------|-------------|
| [autotuning](roles/autotuning/README.md)                     | The autotuning role configures the system and Postgres instances for optimal performances. Most of the configuration values are calculated automatically from available resources found on the system. |
| [init_dbserver](roles/init_dbserver/README.md)               | Initialize the EPAS/PostgreSQL cluster (data) directory. |
| [install_dbserver](roles/install_dbserver/README.md)         | Install EPAS/PostgreSQL database server packages. |
| [manage_dbserver](roles/manage_dbserver/README.md)           | Manage EPAS/PostgreSQL clusters and covers common tasks. |
| [manage_pgbouncer](roles/manage_pgbouncer/README.md)         | Manage PgBouncer pools list and users. |
| [manage_pgpool2](roles/manage_pgpool2/README.md)             | Manage Pgpool-II settings and users. |
| [setup_barman](roles/setup_barman/README.md)                 | Set up EPAS/PostgreSQL backups with Barman. |
| [setup_barmanserver](roles/setup_barmanserver/README.md)     | Set up Barman (Postgres backup) server. |
| [setup_dbt2](roles/setup_dbt2/README.md)                     | Set up a database server for DBT-2. |
| [setup_dbt2_client](roles/setup_dbt2_client/README.md)       | Set up a client (a.k.a. transaction manager) for the client DBT-2. |
| [setup_dbt2_driver](roles/setup_dbt2_driver/README.md)       | Set up emulated terminals (a.k.a. driver) for DBT-2. |
| [setup_dbt3](roles/setup_dbt3/README.md)                     | Install the DBT-3 benchmark kit. |
| [setup_dbt7](roles/setup_dbt7/README.md)                     | Install the DBT-7 benchmark kit. |
| [setup_efm](roles/setup_efm/README.md)                       | Set up EDB Failover Manager (EFM) for PostgreSQL/EPAS HA cluster. |
| [setup_hammerdb](roles/setup_hammerdb/README.md)             | Install HammerDB. |
| [setup_hammerdbserver](roles/setup_hammerdbserver/README.md) | Set up a server for HammerDB. |
| [setup_pemagent](roles/setup_pemagent/README.md)             | Set up Postgres Enterprise Manager (PEM) agent on the Postgres servers. |
| [setup_pemserver](roles/setup_pemserver/README.md)           | Set up Postgres Enterprise Manager (PEM) server. |
| [setup_pgbouncer](roles/setup_pgbouncer/README.md)           | Set up PgBouncer connection pooler. |
| [setup_pgpool2](roles/setup_pgpool2/README.md)               | Set up Pgpool-II connection pooler/load balancer. |
| [setup_replication](roles/setup_replication/README.md)       | Set up the data replication (synchronous/asynchronous). |
| [setup_repmgr](roles/setup_repmgr/README.md)                 | Set up Repmgr for PostgreSQL/EPAS HA cluster. |
| [setup_repo](roles/setup_repo/README.md)                     | Set up the EDB, PostgreSQL Community and EPEL repositories. |
| [setup_touchstone](roles/setup_touchstone/README.md)         | Set up additional packages and software for characterizing system performance. |
| [manage_dbpatches](roles/manage_dbpatches/README.md)             | Manage applying patches on dbservers part of EFM cluster. |


## Pre-Requisites

For correctly installed and configuration of the cluster following are requirements:

  1. Ansible (on the machine on which playbook will be executed).
  2. Operating system privileged user (user with sudo privilege) on all the
     servers/virtual machines.
  3. Machines for the Postgres or EPAS cluster should have at least 2 CPUs and
     4 GB of RAM
  4. The machine utilized for deploying with ansible can be a minimal instance

## Installation

* To install Ansible: **[Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)**

The `edb_ansible` Ansible collection can be installed in 3 different approaches:

### Installing the `edb_postgres` Ansible Collection from Ansible Galaxy

Installing the `edb_postgres` Ansible Collection is done by following the steps
below:

  * Open the command line
  * Type:
    ```bash
    $ ansible-galaxy collection install edb_devops.edb_postgres --force
    ```
  * Press *Enter*

This approach automatically makes the `edb_postgres` collection available to
your playbooks.

A message indicating where the collection is installed will be displayed by
ansible-galaxy. The collection code should be automatically made readily
available for you.

By default the location of your installed collection is:
`~/.ansible/collections/ansible_collections`

### Downloading the `edb-ansible` repository source code from the repository in GitHub

This method requires to have the `ansible-galaxy` tool installed.

Downloading the code from the repository can be accomplished by following the
steps below:

  * Navigate to the repository address: `https://github.com/EnterpriseDB/edb-ansible`
  * Click on the green *Code* Button located next to the *About* section
  * Click on the *Download Zip* Link menu option

After the code has been downloaded, the code will be available as a zip file
which requires being unzipped to your desired target destination.

After the code has been unzipped, you must go to root folder
`edb-ansible-master`, and install the collection by entering the command below:

```bash
$ make install
```

This approach automatically makes the `edb_postgres` collection available to
your playbooks.

A message indicating where the collection is installed will be displayed by
ansible-galaxy. The collection code should be automatically made readily
available for you.

By default the location of your installed collection is:
`~/.ansible/collections/ansible_collections`

### Cloning the `edb-ansible` repository source code from the repository GitHub

This method requires to have the `ansible-galaxy` tool installed.

Downloading the code from the repository can be accomplished by following the
steps below:

```bash
$ git clone git@github.com:EnterpriseDB/edb-ansible.git
```

After the code has been downloaded, the code will be available in your current
directory within a directory named: `edb-ansible`.

You can access the root folder of the repository by entering the command below:

```bash
$ cd edb-ansible
```

You can install the collection by entering the command below:

```bash
$ make install
```

This approach automatically makes the `edb_postgres` collection available to
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
    pemserver:
      hosts:
        pemserver1:
          ansible_host: 110.0.0.4
          private_ip: 10.0.0.4
    primary:
      hosts:
        primary1:
          ansible_host: 110.0.0.1
          private_ip: 10.0.0.1
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
    standby:
      hosts:
        standby1:
          ansible_host: 110.0.0.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
        standby2:
          ansible_host: 110.0.0.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
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
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "EPAS"
        repo_username: "<edb-package-repository-username>"
        repo_password: "<edb-package-repository-password>"
        repo_token: "<edb-package-repository-token>"
        disable_logging: false

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: install_dbserver
      when: "'install_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: init_dbserver
      when: "'init_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_replication
      when: "'setup_replication' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_efm
      when: "'setup_efm' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_pgpool2
      when: "'setup_pgpool2' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: manage_pgpool2
      when: "'manage_pgpool2' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: manage_dbserver
      when: "'manage_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_pemserver
      when: "'setup_pemserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_pemagent
      when: "'setup_pemagent' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_pgbouncer
      when: "'setup_pgbouncer' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: manage_pgbouncer
      when: "'manage_pgbouncer' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_barmanserver
      when: "'setup_barmanserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_barman
      when: "'setup_barman' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: autotuning
      when: "'autotuning' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

You can customize the above example to install PostgreSQL, EPAS, EFM or PEM or
limit what roles you would like to execute.

### Access to EDB's package repository

By default, the `setup_repo` role requires to define credentials (variables
`repo_username` and `repo_password` or `repo_token`) that will be used to configure the access
to EDB's package repository. Having access to EDB package repository is
necessary to deploy EDB softwares like EPAS, EFM or PEM.

When deploying softwares coming only from the community repository (PGDG) like
PostgreSQL, barman or pgbouncer, it's not needed to configure access to EDB's
repository. To disable it, the variable `enable_edb_repo` must be set to
`false`.

## Default user and passwords

The following will occur should a password not be provided for the following
accounts:

  * `pg_superuser`
  * `pg_replication_user`
  * `pg_efm_user`
  * `pg_pem_agent_user`
  * `pg_pem_admin_user`

**Note:**

  * The `~/.edb` folder and contained files are secured by assigning the
    permissions to `user` executing the playbook.
  * A password of 20 characters will be automatically created under: `~/.edb`
    folder.
  * The naming convention for the password file is: `<username>_pass`

## Playbook examples

Examples of utilizing the playbooks for installing: PostgresSQL, EPAS, etc..
are provided and located within the `playbook-examples` directory.

## SSH port configuration

When using non standard SSH port (different from 22), the port value must be
set in two places:
- in the inventory file, for each host, with the host var. `ansible_port`
- in the playbook or variable file with the variable `ssh_port`

## Playbook execution examples

```bash
# To deploy community Postgres version 13
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_version=13 pg_type=PG enable_edb_repo=false"
```
```bash
# To deploy EPAS version 12 with the user ec2-user
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_version=12 pg_type=EPAS repo_username=<edb-repo-username> repo_password=<edb-repo-password>"
# OR
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_version=12 pg_type=EPAS repo_token=<edb-repo-token>"

```

## Database engines supported

### PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
### EnterpriseDB Postgres Advanced Server

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |               :x:|               :x:|               :x:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not tested and not supported

## License

BSD

## Author information

Authors:
  * Doug Ortiz
  * Vibhor Kumar
  * Julien Tachoires
  * Mark Wong
  * Vincent Phan

Contact: **edb-devops@enterprisedb.com**
