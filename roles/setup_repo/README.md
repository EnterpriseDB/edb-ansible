# setup_repo

This Ansible Galaxy Role sets up and configures the repositories from which
packages will be retrieved for any PostgresSQL or EnterpriseDB Postgres
Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
Should there be a need to install and/or configure a PostgreSQL or EnterpriseDB
Postgres Advanced Server Cluster you can utilize the **install_dbserver** role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependency required for this ansible galaxy role is:

  1. Ansible

## Role variables

When executing the role via ansible these are the required variables:

  * ***pg_type***

  Database Engine supported are: PG and EPAS

  * ***yum_username***

  If you have `pg_type` = EPAS, then you need to include `yum_username`

  * ***yum_password***

  If you have `pg_type` = EPAS, then you need to include `yum_password`

The rest of the variables can be configured and are available in the:

  * [roles/setup_repo/defaults/main.yml](./defaults/main.yml) 

## Dependencies

The `setup_repo` role does not have any dependencies on any other roles.

## Example Playbook

### Hosts file content

Content of the `hosts.yml` file:    

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
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### User defined variables

Defining variables can be done using a dedicated file and including this file
 at execution time with the `ansible-playbook` CLI option:

   * `--extra-vars=@./vars.yml`

Content example of the `vars.yml` file:

```yaml
---
pg_type: "PG"
pg_version: 13
yum_username: "xxxxxxxx"
yum_password: "xxxxxxxx"
```

### How to include the `setup_repo` role in your Playbook

Below is an example of how to include the `setup_repo` role:

```yaml
---
- hosts: all
  name: Setup Postgres Repositories
  become: yes
  gather_facts: yes
  roles:
    - setup_repo
```

Defining and adding variables can also be done in the `set_fact` of the
`pre-tasks`.

All the variables are available at:

  - [roles/setup_repo/defaults/main.yml](./defaults/main.yml) 

## Database engines supported

### Community PostgreSQL

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|

### Enterprise DB Postgres Advanced Server

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :x:| :x:| :white_check_mark:|:white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported

## Playbook execution examples

```bash
# To setup community repos. access on CentOS7 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="os=CentOS7 pg_type=PG "
```
```bash
# To setup EDB repos. access on RHEL8 hosts with the user ec2-user
$ ansible-playbook playbook.yml \
  -u ec2-user \
  --private-key <key.pem> \
  --extra-vars="os=RHEL8 pg_type=EPAS yum_username=<username> yum_password=<password>"
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
