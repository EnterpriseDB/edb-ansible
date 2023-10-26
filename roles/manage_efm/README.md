# manage_efm

This Ansible Galaxy Role for managing EFM versions: 3.10 and 4.0 parameters on instances
previously configured.

**Note:**
The role only installs EPAS: 10, 11, 12, 13, 14 or 15 along with EFM: 3.10 or 4.x
across multiple nodes.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
The role does not configure EDB Postgres Advanced Server or PostgreSQL for
replication it only helps in managing EFM cluster parameters across
multiple nodes for EFM monitornig and HA
management.

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
  6. `edb_devops.edb_postgres` -> `setup_replication` - for creating the standby.
  7. `edb_devops.edb_postgres` -> `setup_efm` - for setting up EFM cluster

## Role variables

When executing the role via ansible there are three required variables:

  * ***os***

  Operating Systems supported are: CentOS7, RHEL7, CentOS8, RHEL8, Debian10, Ubuntu20, Ubuntu22, and AlmaLinux8

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13, 14 and 15

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `manage_efm` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/manage_efm/defaults/main.yml](./defaults/main.yml) 
  * [roles/manage_efm/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  * [roles/manage_efm/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/manage_efm/vars/PG_Debian.yml](./vars/PG_Debian.yml) 
  * [roles/manage_efm/vars/PG_RedHat.yml](./vars/PG_RedHat.yml) 

## Dependencies

The `manage_efm` role does not have any dependencies on any other roles.

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

### How to include the `manage_efm` role in your Playbook

Below is an example of how to include the `manage_efm` role:

```yaml
---
- hosts: primary,standby
  name: Install EFM on Instances
  become: true
  gather_facts: yes
  any_errors_fatal: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_type: "PG"
        pg_version: 14

        efm_version: 4.0
        efm_parameters:
          - name: script.notification
            value: "/usr/edb/efm-4.0/bin/notification.sh"

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
    - role: manage_efm
      when: "'manage_efm' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  - [roles/manage_efm/defaults/main.yml](./defaults/main.yml) 
  - [roles/manage_efm/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  - [roles/manage_efm/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  - [roles/manage_efm/vars/PG_Debian.yml](./vars/PG_Debian.yml) 
  - [roles/manage_efm/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)

## Database engines supported

### Community PostgreSQL and EFM 3.10/4.x

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
### EnterpriseDB Postgres Advanced Server and EFM 3.10/4.x

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

## Playbook execution examples

```bash
# To deploy community Postgres version 14 on CentOS7 hosts with the user centos
# EFM version 4.4
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=14 pg_type=PG efm_version=4.4"
```
```bash
# To deploy EPAS version 12 on RHEL8 hosts with the user ec2-user EFM version
# 3.10
$ ansible-playbook playbook.yml \
  -u ec2-user \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=12 pg_type=EPAS efm_version=3.10"
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
