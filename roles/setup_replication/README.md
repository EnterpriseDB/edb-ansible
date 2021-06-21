# setup_replication

This Ansible Galaxy Role configures Replication on PostgresSQL or EnterpriseDB
Postgres Advanced Server versions: 10, 11, 12 and 13 on instances previously
configured.

## Requirements

The requirements for this ansible galaxy role are:

  1. Ansible
  2. `community.general` - utilized when creating aditional users during a
     Postgres Install. Only on primary nodes.
  3. `edb_devops.edb_postgres` -> `setup_repo` - for repository installation
  4. `edb_devops.edb_postgres` -> `install_dbserver` - for installation of
     PostgreSQL/EPAS binaries.
  5. `edb_devops.edb_postgres` -> `init_dbserver` - for the initialization of
     primary server

## Role variables

When executing the role via ansible there are three required variables:

  * ***os***

  Operating Systems supported are: CentOS7 and RHEL7

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

The rest of the variables can be configured and are available in the:

  * [roles/setup_replication/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_replication/vars/EPAS.yml](./vars/EPAS.yml)
  * [roles/setup_replication/vars/PG.yml](./vars/PG.yml)

## Dependencies

The `setup_replication` role does not have any dependencies on any other roles.

## Example Playbook

### Hosts file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### How to include the `setup_replication` role in your Playbook

Below is an example of how to include the `setup_replication` role:

```yaml
---
- hosts: standby
  name: Setup Postgres replication on Instances
  become: true
  gather_facts: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"

  roles:
    - setup_replication
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_replication/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_replication/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/setup_replication/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  * [roles/setup_replication/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_replication/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Database engines supported

### Community PostgreSQL

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x:| :x: | :x: |  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x: | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x: | :x: | :white_check_mark:| :white_check_mark:|

### Enterprise DB Postgres Advanced Server

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :x:| :x:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:| :white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x:| :x: | :x: |  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x: | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x: | :x: | :white_check_mark:| :white_check_mark:|

## Playbook execution examples

```bash
# To deploy community Postgres version 13 on CentOS7 hosts with the user centos
# EFM version 4.0
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=13 pg_type=PG efm_version=4.0"
```
```bash
# To deploy EPAS version 12 on RHEL8 hosts with the user ec2-user EFM version
# 3.10
$ ansible-playbook playbook.yml \
  -u ec2-user \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="os=RHEL8 pg_version=12 pg_type=EPAS efm_version=3.10"
```

## License

BSD

## Author information

Author:

  * EDB Postgres - www.enterprisedb.com
