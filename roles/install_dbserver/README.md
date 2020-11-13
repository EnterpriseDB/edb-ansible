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

  * ***os***

  Operating Systems supported are: CentOS7, RHEL7, CentOS8 and RHEL8

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

### Hosts file content

Content of the `hosts.yml` file:

```yaml
---
servers:
  main1:
    node_type: primary
    public_ip: xxx.xxx.xxx.xxx
  standby11:
    node_type: standby
    public_ip: xxx.xxx.xxx.xxx
  standby12:
    node_type: standby
    public_ip: xxx.xxx.xxx.xxx
```

### How to include the `install_dbserver` role in your Playbook

Below is an example of how to include the `install_dbserver` role:

```yaml
---
- hosts: localhost
  name: Install Postgres on Instances
  become: true
  gather_facts: no
 
  collections:
    - edb_devops.postgres

  vars_files:
    - hosts.yml

  pre_tasks:
    # Define and assign any variables that
    # have been previously defined in role
    # or that are new
    - name: Initialize the user defined variables
      set_fact:
        os: "CentOS7"
        pg_type: "PG"
        pg_version: 12

  roles:
    - install_dbserver
```

Defining and adding variables can be done in the `set_fact` of the `pre-tasks`.

## Database engines supported

### Community Postgresql

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|

### Enterprise DB Postgresql Advanced Server

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :x:| :x:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|

- :white_check_mark: - Tested and supported

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
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * DevOps
  * doug.ortiz@enterprisedb.com www.enterprisedb.com
