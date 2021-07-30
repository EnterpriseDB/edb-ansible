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

  * ***repo_username***

  If you have `pg_type` = EPAS, then you need to include `repo_username`

  * ***repo_password***

  If you have `pg_type` = EPAS, then you need to include `repo_password`

  * ***yum_additional_repos***

  List of additional YUM repositories. List items are dictionnaries:

    * *name*: Repository name
    * *description*: Repository description
    * *baseurl*: Repository URL
    * *gpgkey*: GPG key locatio. Default: None
    * *gpgcheck*: Enable package signature checking with GPG. Default: false

  * **apt_additional_repos**

  List of additional APT repositories. List items are dictionnaries:

    * *repo*: Debian repository connection string
    * *filename*: Repository file name on disk: `<filename>.list`


The rest of the variables can be configured and are available in the:

  * [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `setup_repo` role does not have any dependencies on any other roles.

## Example Playbook

### Inventory file content

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

### How to include the `setup_repo` role in your Playbook

Below is an example of how to include the `setup_repo` role:

```yaml
---
- hosts: all
  name: Setup Postgres Repositories
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 13
        pg_type: "PG"
        repo_username: "xxxxxxxx"
        repo_password: "xxxxxxxx"
        # Additional repositories
        yum_additional_repos:
          - name: "Additional Repo. 1"
            description: "Description of the repo."
            baseurl: https://my.repo.internal/CentOS$releasever-$basearch
            gpgkey: https://my.repo.internal/key.asc
            gpgcheck: true
          - name: "Local Repo"
            baseurl: file:///opt/my_local_repo

  roles:
    - setup_repo
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

## Database engines supported

### Community PostgreSQL

| Distribution | 10 | 11 | 12 | 13 |
| ------------------------- |:--:|:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x:| :x:| :x:|  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x:| :x:| :white_check_mark:| :white_check_mark:| 

### Enterprise DB Postgres Advanced Server

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Centos 8 | :x:| :x:| :white_check_mark:|:white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 | :x:| :x:| :x:|  :white_check_mark:|
| Debian 9 (Stretch) - x86_64 | :x:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian 10 (Buster) - x86_64 | :x:| :x:| :white_check_mark:| :white_check_mark:| 


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
  --extra-vars="os=RHEL8 pg_type=EPAS repo_username=<username> repo_password=<password>"
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
