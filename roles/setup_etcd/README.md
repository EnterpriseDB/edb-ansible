# Setup ETCD

This Ansible Galaxy Role installs and configure ETCD for Patroni cluster setup.

Note: The role by default installs 3.5.6

Not all Distribution or versions are supported on all the operating systems available.

Note: The role does not configure EDB Postgres Advanced Server or PostgreSQL for replication it only installs ETCD across multiple nodes.

The ansible playbook must be executed under an account that has full privileges.

## Requirements

The requirements for this ansible galaxy role are:

  1. Ansible >= 2.9
  2. `community.general`
  3. `edb_devops.edb_postgres` -> `setup_repo` - for installing the EPAS/PG
     repository
  4. Access etcd RPM/download URL mentioned in [default/main] (./defaults/main.yml)

## Role Variables

When executing the role via ansible there are three required variables:

  * ***os***

  Operating Systems supported are: CentOS7, RHEL7, CentOS8, RHEL8, AlmaLinux8, Debian10 and Ubuntu20

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13, 14 and 15

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_etcd` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_etcd/defaults/main.yml](./defaults/main.yml) 
  * [roles/setup_etcd/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/setup_etcd/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_etcd/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  * [roles/setup_etcd/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Dependencies

The `setup_etcd` role does not have any dependencies on any other roles.

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
### How to include the `setup_etcd` role in your Playbook

Below is an example of how to include the `setup_etcd` role:

```yaml
---
- hosts: primary,standby
  name: Install ETCD on Instances
  become: true
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        etcd_version: 3.5.6
        etcd_architecture: "amd64"

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_etcd
      when: "'setup_etcd' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  - [roles/setup_etcd/defaults/main.yml](./defaults/main.yml)
  - [roles/setup_etcd/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  - [roles/setup_etcd/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  - [roles/setup_etcd/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  - [roles/setup_etcd/vars/PG_Debian.yml](./vars/PG_Debian.yml)

## Database engines supported

### Community PostgreSQL and ETCD

### PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |               15 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| AlmaLinux8                        |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
### EnterpriseDB Postgres Advanced Server 

| Distribution                      |               10 |               11 |               12 |               13 |               14 |               15 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| AlmaLinux8                        |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |               :x:|               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported


## License

BSD

## Author Information

Author:
  * Vibhor Kumar (Co-Author)
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb.com www.enterprisedb.com
