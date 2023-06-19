# setup_pgbackrest

This role is for setting up pgBackRest backups on Postgres nodes.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.
  3. `edb_devops.edb_postgres` -> `setup_pgbackrestserver` role to set up the pgbackrestserver.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 13, 14 and 15

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_pgbackrest` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_pgbackrest/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `replication_user`

Dedicated replication user used in WAL streaming replication. Default: `repuser`

Example:
```yaml
replication_user: 'repuser'
```

### `pgbackrest_spool_directory`

pgBackRest spool directory. Stores transient data during backup and recovery. Only used when `pgbackrest_archive_method` set to `async`. Default: `/var/spool/pgbackrest`

Example:
```yaml
pgbackrest_spool_directory: '/var/spool/pgbackrest'
```

### `process_max_backup`

Number of parallel processes used during backup. Not recommended to use more than 25% of available CPU. Only used when 
`pgbackrest_archive_method` is set to `async`. Default: `3`

Example:
```yaml
process_max_backup: 3
```

### `process_max_recovery`

Number of parallel processes used during recovery. Set as high as possible to allow for fastest recovery time. Only used 
when `pgbackrest_archive_method` is set to `async`. Default: `3`

Example:
```yaml
process_max_recovery: 3
```

## Host Variables

Below are the host variables defined in the inventory file, for each Postgres node we want to backup with pgBackRest.

### `pgbackrest`

Enable pgBackRest backups for the host. Default: `false`

Example:
```yaml
pgbackrest: true
```

### `pgbackrest_server_private_ip`

pgBackRest server private IP address. Default: None

Example:
```yaml
pgbackrest_server_private_ip: 10.0.0.123
```

### `pgbackrest_archive_method`

Archive method. Can be:
  * `standard` for archiving WAL segments one at a time. When a WAL segment is pushed via the `archive_command`, 
     the transfer must be completed before another WAL segment can be archived.   
  * `async` for archiving WAL segments asychronously. WAL segments can be grouped together and transferred at the same 
     time. Can improve archiving efficiency. 

Default: `async`

Example:
```yaml
pgbackrest_archive_method: async
```

## Dependencies

This role does not have any dependencies, but package repositories should have been 
configured beforehand with the `setup_repo` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pgbackrestserver:
      hosts:
        pgbackrest1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          # enable pgBackRest
          pgbackrest: true
          # Private IP address of the pgBackRest server
          pgbackrest_server_private_ip: xxx.xxx.xxx.xxx
          # WAL archiving method 
          pgbackrest_archive_method: async
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          # enable pgBackRest
          pgbackrest: true
          # Private IP address of the pgBackRest server
          pgbackrest_server_private_ip: xxx.xxx.xxx.xxx
          # WAL archiving method 
          pgbackrest_archive_method: async
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          # enable pgBackRest
          pgbackrest: true
          # Private IP address of the pgBackRest server
          pgbackrest_server_private_ip: xxx.xxx.xxx.xxx
          # WAL archiving method 
          pgbackrest_archive_method: async
```

### How to include the `setup_pgbackrest` role in your Playbook

Below is an example of how to include the `setup_pgbackrest` role:

```yaml
---
- hosts: primary, standby
  name: Configure pgBackRest backup on Postgres nodes
  become: yes
  gather_facts: yes
  any_errors_fatal: true

  collections: 
    - edb_devops.edb_postgres
    
  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"
        
  roles:
    - role: setup_pgbackrest
      when: "'setup_pgbackrest' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_pgbackrest/defaults/main.yml](./defaults/main.yml)

## License

BSD

## Author information

Author:

  * Hannah Stoik
  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com