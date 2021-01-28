[![Ansible Lint Status](https://github.com/EnterpriseDB/edb-ansible/workflows/ansible-lint/badge.svg)](https://github.com/EnterpriseDB/edb-ansible/actions?query=workflow%3Aansible-lint)

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

## Roles

### setup_repo

A role for setting up the EDB and PG Community and EPEL repositories. For
installation of these repositories, role needs outbound connections to
internet, mainly connection to the following sites:

```
   1. yum.enterprisedb.com
   2. download.postgresql.org
   3. dl.fedoraproject.org
```

This role requires following compulsory parameters:

  * `pg_type`: "EPAS" or "PG"
  * `yum_username`: EDB repository's username
  * `yum_password`: EDB yum repository's password.

For access to EDB repository, you can use following link:
[EDB yum access](https://www.enterprisedb.com/user/register?destination=/repository-access-request%3Fdestination%3Dnode/1255704%26resource%3D1255704%26ma_formid%3D2098)

### install_dbserver

A role for installing EPAS/PG database server packages. This role installs the
EPAS/PG packages, depending on the values of the following variables in the
playbook.yml:

  1. `pg_type`: EPAS/PG
  2. And `pg_version`: EPAS/PG major version number

### init_dbserver

A role for initializing the PG/EPAS cluster(data) directory.

This role allows users to pass following variables:

  1. `pg_type`: EPAS/PG
  2. `pg_version`: EPAS/PG Version. *Default is 12.*
  3. `pg_data`: EPAS/PG data directory. *Default is /var/lib/edb/as{pg_version}/data*
  4. `pg_wal`: EPAS/PG wal location. *Default is /var/lib/edb/as{pg_version}/data/pg_wal*
  5. `pg_ssl`: For configuration of data directory with SSL

For more information on variables, please refer to the following variables file:

  1. EPAS variables: [roles/init_dbserver/vars/EPAS.yml](./roles/init_dbserver/vars/EPAS.yml)
  2. And, PG variables: [roles/init_dbserver/vars/PG.yml](./roles/init_dbserver/vars/PG.yml)

For more information on the role, please refer roles README
[README.md](./roles/init_dbserver/README.md)

### setup_replication

A role for setting up the replication (synchronous/asynchronous).
Similar to `init_dbserver` role, `setup_replication` has following variables
for managing the EPAS/PG.

  1. `pg_type`: EPAS/PG
  2. `pg_version`: EPAS/PG Version. *Default is 12.*
  3. `pg_data`: EPAS/PG data directory. *Default is /var/lib/edb/as{pg_version}/data*
  4. `pg_wal`: EPAS/PG wal location. *Default is /var/lib/edb/as{pg_version}/data/pg_wal*
  5. `pg_replication_user`: Replication user for replicating data between
      primary and standby. *Default is repuser*
  6. `pg_replication_user_password`: Replication user password.
      *Default auto generated and stored on localhost under `~/.edb/<pg_replication_user_password>_pass`*

For more information on the role, please refer roles README
[README.md](./roles/setup_replication/README.md)

### setup_efm

A role for setting up EDB Failover Manager for Postgres/EPAS HA cluster.

In the playbook, user can choose the specific roles based on their requirement.
For more information on the role, please refer roles README
[README.md](./roles/setup_efm/README.md)

### setup_pemserver

This role helps in setting PEM Server.
For more information on the role, please refer roles README
[README.md](./roles/setup_pemserver/README.md)

### setup_pemagent

This role helps in setting and deployment of PEM Agent on the
PG/EPAS servers.
For more information on the role, please refer roles README
[README.md](./roles/setup_pemagent/README.md)

### manage_dbserver

This role helps in managing the HA cluster and covers common tasks.
For more information on the role, please refer roles README
[README.md](./roles/manage_dbserver/README.md)

### setup_pgbouncer

This role install and configure a new PgBouncer connection pooler.
For more information on the role, please refer roles README
[README.md](./roles/setup_pgbouncer/README.md)

### manage_pgbouncer

This role helps in managing PgBouncer connection pools list and users.
For more information on the role, please refer roles README
[README.md](./roles/manage_pgbouncer/README.md)

### setup_pgpool2

This role install and configure a new PgpoolII connection pooler.
For more information on the role, please refer roles README
[README.md](./roles/setup_pgpool2/README.md)

### manage_pgpool2

This role helps in managing Pgpool II user list and configuration.
For more information on the role, please refer roles README
[README.md](./roles/manage_pgpool2/README.md)

### setup_barmanserver

Setting up Barman server role.
[README.md](./roles/setup_barmanserver/README.md)

### setup_barman

Configure Postgres backups with Barman.
[README.md](./roles/setup_barman/README.md)

### autotuning

The autotuning role configures the system and Postgres instances for optimal
performances. Most of the configuration values are calculated automatically
from available resources found on the system.
[README.md](./roles/autotuning/README.md)

## Pre-Requisites

For correctly installed and configuration of the cluster following are requirements:

  1. Following are ports which should be opened for communication between the
     servers:

    * Postgres:                           **5432**
    * EDB Postgres Advanced Server Port:  **5444**
    * EDB Failover Manager:               **7800-7810**

  **Note**: If you have firewall enabled on the server, then please allow the
  access through above ports.

  2. Ansible (on the machine on which playbook will be executed).
  3. Operating system privileged user (user with sudo privilege) on all the
     servers/virtual machines.
  4. Instances for the Postgres or EPAS cluster should have at least 2 CPUs and
     4 GB of RAM
  5. The instance utilized for deploying with ansible can be a minimal instance

**Note**: In our examples, we have used `centos` user for Centos OS and
`ec2_user` for RHEL OS as a privileged user.

## Installation

* To install Ansible: **[Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)**
* A CLI or SDK depending on the Cloud vendor to utilize is required:
  * To install the Amazon Web Services CLI please refer to: **[Installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)**
  * To install the Microsoft Azure CLI please refer to: **[Installing the AZURE CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)**
  * To install the Google Cloud SDK please refer to: **[Installing the Google Cloud SDK](https://cloud.google.com/sdk/docs/downloads-interactive)**

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

## Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pemserver:
      hosts:
        pemserver1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
```

## How to include the roles in your Playbook

Below is an example of how to include all the roles for a deployment in a
playbook:

```yaml
---
- hosts: all
  name: Postgres deployement playbook
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"
        yum_username: ""
        yum_password: ""
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

You can customize the above example to install Postgres, EPAS, EFM or PEM or
limit what roles you would like to execute.

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

Examples of utilizing the playbooks for installing: Postgres, EnterpriseDB
Postgres Advanced Server, Centos7 or RHEL7 are provided and located within the
`playbook-examples` directory.

## Playbook execution examples

```bash
# To deploy community Postgres version 13 with the user centos
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="pg_version=13 pg_type=PG"
```
```bash
# To deploy EPAS version 12 with the user ec2-user
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u ec2-user \
  --private-key <key.pem> \
  --extra-vars="pg_version=12 pg_type=EPAS yum_username=xxxxx yum_password=xxxxx"
```

## Database engines supported

### Community PostgreSQL

| Distribution | 10 | 11 | 12 | 13|
| ------------------------- |:--:|:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian | :x: | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: | :x: |

### Enterprise DB Postgres Advanced Server

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :x:| :x:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|
| Debian | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: |

- :white_check_mark: - Tested and supported
- :x: - Not tested and not supported

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * Julien Tachoires
  * Vibhor Kumar
  * Collection Name: postgres
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
