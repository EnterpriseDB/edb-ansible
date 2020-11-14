# setup_pem

This Ansible Galaxy Role Installs and configure PEM on Instances previously
configured.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
The role does not configure EDB Postgres Advanced Server or PostgreSQL for
replication it only installs Postgres Enterprise Manager (PEM) agents across
multiple nodes and configure database nodes for PEM monitornig and configures
any node to be a PEM server.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The requirements for this ansible galaxy role are:

  1. Ansible >= 2.9
  2. `community.general`
  3. `edb_devops.postgres` -> `setup_repo` - for installing the EPAS/PG
     repository
  4. `edb_devops.postgres` -> `install_dbserver` - for installing the EPAS/PG
     binaries
  5. `edb_devops.postgres` -> `init_dbserver` - for initializing the EPAS/PG
     data directory and configuring a primary node.

## Role variables

When executing the role via ansible there are three required variables:

  * ***os***

  Operating Systems supported are: CentOS7 and RHEL7

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

The rest of the variables can be configured and are available in the:

  * [roles/setup_pem/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `setup_pem` role does not have any dependencies on any other roles.

## Example Playbook

### Hosts file content

Content of the `hosts.yml` file:

```yaml
---
servers:
  pemserver:
    node_type: pemserver
    private_ip: xxx.xxx.xxx.xxx
    public_ip: xxx.xxx.xxx.xxx
  main:
    node_type: primary
    pem_agent: true
    private_ip: xxx.xxx.xxx.xxx
    public_ip: xxx.xxx.xxx.xxx
  standby1:
    node_type: standby
    pem_agent: true
    replication_type: asynchronous
    private_ip: xxx.xxx.xxx.xxx
    public_ip: xxx.xxx.xxx.xxx
  witness:
    node_type: witness
    pem_agent: true
    private_ip: xxx.xxx.xxx.xxx
    public_ip: xxx.xxx.xxx.xxx
```


## How to include the `setup_pem` role in your Playbook

Below is an example of how to include the `setup_pem` role:

```yaml
---
- hosts: localhost
  name: Setup PEM on Instances
  become: true
  gather_facts: no

  collections:
    - edb_devops.edb_postgres

  vars_files:
    - hosts.yml

  pre_tasks:
    # Define or re-define any variables previously assigned
    - name: Initialize the user defined variables
      set_fact:
        os: "CentOS7"
        pg_type: "PG"
        pg_version: "12"
  roles:
    - setup_pem
```

Two example playbooks for setting up PEM with CentOS7 and RHEL7 are available
in the [playbook-examples](/playbook-examples) directory.

Defining and adding variables can be done in the `set_fact` of the `pre-tasks`.

All the variables are available at:

  - [roles/setup_pem/vars/EPAS.yml](./vars/EPAS.yml) 
  - [roles/setup_pem/vars/PG.yml](./vars/PG.yml) 

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
# To deploy community Postgres version 13 on CentOS7 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="os=CentOS7 pg_version=13 pg_type=PG"
```
```bash
# To deploy EPAS version 12 on RHEL8 hosts with the user ec2-user
$ ansible-playbook playbook.yml \
  -u ec2-user \
  --private-key <key.pem> \
  --extra-vars="os=RHEL8 pg_version=12 pg_type=EPAS"
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * Vibhor Kumar (Co-Author)
  * EDB Postgres
  * DevOps
  * doug.ortiz@enterprisedb.com www.enterprisedb.com
