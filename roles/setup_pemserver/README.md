# setup_pemserver

This Ansible Galaxy Role Installs and configure PEM server.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
The role does not configure EDB Postgres Advanced Server or PostgreSQL for
replication it only installs Postgres Enterprise Manager (PEM) and configures
any node to be a PEM server.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The requirements for this ansible galaxy role are:

  1. Ansible >= 2.9
  2. `community.general`
  3. `edb_devops.edb_postgres` -> `setup_repo` - for installing the EPAS/PG
     repository
  4. `edb_devops.edb_postgres` -> `install_dbserver` - for installing the EPAS/PG
     binaries
  5. `edb_devops.edb_postgres` -> `init_dbserver` - for initializing the EPAS/PG
     data directory and configuring a primary node.

## Role variables

When executing the role via ansible there are three required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

The rest of the variables can be configured and are available in the:

  * [roles/setup_pemserver/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `setup_pemserver` role does not have any dependencies on any other roles.

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

## How to include the `setup_pemserver` role in your Playbook

Below is an example of how to include the `setup_pemserver` role:

```yaml
---
- hosts: pemserver
  name: Setup PEM server
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
    - setup_pemserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  - [roles/setup_pemserver/defaults/main.yml](./defaults/main.yml) 
  - [roles/setup_pemserver/vars/EPAS.yml](./vars/EPAS.yml) 
  - [roles/setup_pemserver/vars/PG.yml](./vars/PG.yml) 

## Database engines supported

### Community PostgreSQL and PEM

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|

### Enterprise DB Postgresql Advanced Server and PEM

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :x:| :x:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported

## Playbook execution examples

```bash
# To deploy community Postgres version 13 with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=13 pg_type=PG"
```
```bash
# To deploy EPAS version 12 with the user ec2-user
$ ansible-playbook playbook.yml \
  -u ec2-user \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=12 pg_type=EPAS"
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * Vibhor Kumar (Co-Author)
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb.com www.enterprisedb.com
