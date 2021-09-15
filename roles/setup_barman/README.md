# setup_barman

This role is for configuring Barman backups on Postgres nodes.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `setup_barman` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_barman/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `barman_pg_user`

Dedicated Postgres user excuting barman queries. Default: `barman`

Example:
```yaml
barman_pg_user: 'barman'
```

## Host Variables

Below are the host variables defined in the inventory file, for each Postgres
node we want to backup with Barman.

### `barman`

Enable Barman backups for the host. Default: `false`

Example:
```yaml
barman: yes
```

### `barman_server_private_ip`

Barman server private IP address. Default: None

Example:
```yaml
barman_server_private_ip: 10.0.0.123
```

### `barman_backup_method`

Backup method. Can be:

  * `postgres` for backups based on `pg_basebackup` using Streaming
    Replication protocol.
  * `rsync` for backups based on the `rsync` command using SSH protocol.

Default: `rsync`

Note: `rsync` backups can only be proceeded on primary nodes. Backuping
standby nodes must be done with the `postgres` backup method.

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    barmanserver:
      hosts:
        barman1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          barman: true
          barman_server_private_ip: xxx.xxx.xxx.xxx
          barman_backup_method: rsync
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          barman: true
          barman_server_private_ip: xxx.xxx.xxx.xxx
          barman_backup_method: postgres
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          barman: true
          barman_server_private_ip: xxx.xxx.xxx.xxx
          barman_backup_method: postgres
```

### How to include the `setup_barman` role in your Playbook

Below is an example of how to include the `setup_barman` role:
```yaml
---
- hosts: primary, standby
  name: Configure Barman backup on Postgres nodes
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
    - setup_barman
      when: "'setup_barman' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_barman/defaults/main.yml](./defaults/main.yml)

## Important notes for recovery

This role adds the `recovery_options=get-wal` to the barman configuration file,
this implies that the server where a backup is restored is able to access barman
with ssh.
If no ssh access is possible to the Barman server from the new PostgreSQL server
then it is required to execute the recovery with: `--no-get-wal` parameter, like:
```bash
$ barman recover --no-get-wal \
     --remote-ssh-command 'ssh postgresql@restore_server' \
     my_server_instance \
     latest /path/to/new/pgdata
```

`get-wal` allows to recover partial WAL file from the backup when streaming
backup is used (i.e. the one being currently written by the backuped PostgreSQL
server).

`barman recover --no-get-wal` requires `recovery_options=get-wal` to be set.

## License

BSD

## Author information

Author:

  * Cédric Villemain
  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
