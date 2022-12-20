# Role Name

An Ansible role which installs and configures Patroni - HA solution for PostgreSQL/EPAS.

**Note:**
The role only installs EPAS: 10, 11, 12, 13 or 14
across multiple nodes.

**Not all Distribution or versions are supported on all the operating systems
available.**

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

## Role Variables

When executing the role via ansible there are three required variables:

  * ***os***

  Operating Systems supported are: CentOS7, RHEL7, CentOS8, RHEL8, Debian10 and Ubuntu20

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13 and 14

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_patroni` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_patroni/defaults/main.yml](./defaults/main.yml) 
  * [roles/setup_patroni/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/setup_patroni/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)

## Dependencies

`setup_patroni` has dependencies on the following roles
  1. `setup_repo`
  2. `install_dbserver`
  3. `setup_etcd`

## Example Playbook

### Hosts file content

Content of the `inventory.yml` file:

```yaml
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          etcd: true
          etcd_cluster_name: 'patroni-etcd'
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          etcd: true
          etcd_cluster_name: 'patroni-etcd'
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          etcd: true
          etcd_cluster_name: 'patroni-etcd'
```

### How to include the `setup_patroni` role in your Playbook

Below is an example of how to include the `setup_patroni` role:

```yaml
---
- hosts: primary,standby
  name: Install Patroni on Instances
  become: true
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_type: "PG"
        pg_version: 14
        use_patroni: true

  roles:
    - setup_repo
    - install_dbserver
    - setup_etcd
    - setup_patroni
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  - [roles/setup_patroni/defaults/main.yml](./defaults/main.yml)
  - [roles/setup_patroni/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  - [roles/setup_patroni/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)

## Database engines supported

### Community PostgreSQL 

### PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
### EnterpriseDB Postgres Advanced Server

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported

## Playbook execution examples

```bash
# To deploy community Postgres version 14 on CentOS7 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=14 pg_type=PG"
```
```bash
# To deploy EPAS version 12 on RHEL8 hosts with the user ec2-user 
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

  * Vibhor Kumar (Co-Author)
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb.com www.enterprisedb.com
