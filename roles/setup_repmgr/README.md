# setup_repmgr

This Ansible Role installs and configures High-Availability of a streaming
replication Postgres cluster, based on `repmgr`.

**Note:**
Only PostgreSQL is supported by this role, EPAS will be supported in the future.
For more details refer to the: *Database engines supported* section.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The requirements for this Ansible Role are:

  1. Ansible >= 2.9
  2. `community.general`
  3. `edb_devops.edb_postgres` -> `setup_repo` - for installing the EPAS/PG
     repository
  4. `edb_devops.edb_postgres` -> `install_dbserver` - for installing the EPAS/PG
     binaries
  5. `edb_devops.edb_postgres` -> `init_dbserver` - for initializing the EPAS/PG
     data directory and configuring a primary node.
  6. `edb_devops.edb_postgres` -> `setup_replication` - for creating the standby.

## Role variables

When executing the role via ansible there are three required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13, 14 and 15

  * ***pg_type***

  Database Engine supported is PG


These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_repmgr` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_repmgr/defaults/main.yml](./defaults/main.yml) 
  * [roles/setup_repmgr/vars/PG_RedHat.yml](./vars/PG_RedHat.yml) 
  * [roles/setup_repmgr/vars/PG_Debian.yml](./vars/PG_Debian.yml) 

## Dependencies

This role depends on the `manage_dbserver` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file for 3 Postgres nodes cluster composed of 1
primary node and 2 standby nodes:

```yaml
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: 192.168.122.1
          private_ip: 10.0.0.1
    standby:
      hosts:
        standby1:
          ansible_host: 192.168.122.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
        standby2:
          ansible_host: 192.168.122.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
```

The following inventory example illustrates how to deploy a 2 Postgres nodes
composed of 1 primary node, 1 standby node and 1 witness node:

```yaml
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: 192.168.122.1
          private_ip: 10.0.0.1
    standby:
      hosts:
        standby1:
          ansible_host: 192.168.122.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
    witness:
      hosts:
        witness1:
          init_dbserver: true
          ansible_host: 192.168.122.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
```


### How to include the `setup_repmgr` role in your Playbook

Below is an example of how to include the `setup_repmgr` role:

```yaml
---
- hosts: primary,standby,witness
  name: Install and configure Repmgr
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
        
        repmgr_failover: automatic
        repmgr_reconnect_attemps: 2
        repmgr_reconnect_interval: 2

  roles:
    - role: setup_repmgr
      when: "'setup_repmgr' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

## Database engines supported

### Community PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |               15 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported

## Playbook execution examples

```bash
# To deploy community Postgres version 14 on CentOS8 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --private-key <key.pem> \
  --extra-vars="pg_version=14 pg_type=PG"
```

## License

BSD

## Author information

Author:

  * Julien Tachoires (@jt-edb)
