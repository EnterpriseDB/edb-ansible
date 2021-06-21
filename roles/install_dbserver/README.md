# install_dbserver

This Ansible Galaxy Role Installs Postgres or EnterpriseDB Postgresql Advanced
Server versions: 10, 11, 12 and 13 on Instances previously configured. 

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
The role does not configure Postgres nor EnterpriseDB Postgres Advanced Server
for replication it only installs Postgres or EnterpriseDB Postgres Advanced
Server across multiple nodes: Main and Standby.
Should there be a need to configure a Postgres or EnterpriseDB Postgres
Advanced Server Cluster for replication you can utilize the `setup_replication`
role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

  1. Ansible
  2. `community.general` Ansible Module - Utilized when creating aditional
     users during a Postgres Install
  3. `edb_devops.postgres` -> `setup_repo` role for setting the repository on
     the systems

## Role variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `install_dbserver` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `install_dbserver` role does not have any dependencies on any other roles.

## Example Playbook

### Inventory file content

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

### How to include the `install_dbserver` role in your Playbook

Below is an example of how to include the `install_dbserver` role:

```yaml
---
- hosts: primary,standby,pemserver
  name: Install Postgres binaries
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"

  roles:
    - install_dbserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Database engines supported

### Community Postgresql

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x: | :x: | :x: |  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x: | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x: | :x: | :white_check_mark:| :white_check_mark:| 

### Enterprise DB Postgresql Advanced Server

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :x:| :x:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:| :white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x: | :x: | :x: |  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x: | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x: | :x: | :white_check_mark:| :white_check_mark:| 

- :white_check_mark: - Tested and supported

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
  --extra-vars="pg_version=12 pg_type=EPAS"
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * Vibhor Kumar (Reviewer)
  * Julien Tachoires
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb.com www.enterprisedb.com
