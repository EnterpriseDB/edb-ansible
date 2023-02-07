# setup_barman

This role is for configuring Barman backups on Postgres nodes.

## Requirements

Following are the requirements of this role.

1. Ansible
2. `hypersql_devops.postgres` -> `setup_repo` role for setting the repository on
   the systems.

## Role Variables

When executing the role via ansible these are the required variables:

- **_pg_version_**

Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`

- **_pg_type_**

Database Engine supported are: `PG`

These and other variables can be assigned in the `pre_tasks` definition of the
section: _How to include the `setup_barman` role in your Playbook_

The rest of the variables can be configured and are available in the:

- [roles/setup_barman/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `barman_pg_user`

Dedicated Postgres user excuting barman queries. Default: `barman`

Example:

```yaml
barman_pg_user: "barman"
```

## Host Variables

Below are the host variables defined in the inventory file, for each Postgres
node we want to backup with Barman.

### `barman`

Enable Barman backups for the host. Default: `false`

Example:

```yaml
barman: true
```

### `barman_server_private_ip`

Barman server private IP address. Default: None

Example:

```yaml
barman_server_private_ip: 10.0.0.123
```

### `barman_backup_method`

Backup method. Can be:

- `postgres` for backups based on `pg_basebackup` using Streaming
  Replication protocol.
- `rsync` for backups based on the `rsync` command using SSH protocol.

Default: `rsync`

Note: When backing up standby nodes with `backup_method = rsync` the minimum supported version of Barman is 2.8.

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

In the High-Availability context, when using a Virtual IP address for routing
read/write traffic to the primary node, then it's possible to configure barman
to use this VIP address as Postgres connection endpoint. This way, in case of
timeline change (following a failover or switchover event), barman will be able
to automatically fetch new WAL records coming from the new primary node,
without requiring any manual operation.

This configuration is only possible when using the `postgres` backup method,
which is based on backup and WAL archiving using streaming replication.

Above is an example of inventory file implementing this type of configuration:

```yaml
---
all:
  children:
    barmanserver:
      hosts:
        barman:
          ansible_host: 192.168.122.2
          private_ip: 192.168.122.2
    primary:
      hosts:
        pg1:
          ansible_host: 192.168.122.3
          private_ip: 192.168.122.3
          # Enable barman
          barman: true
          # Private IP address of the barman server
          barman_server_private_ip: 192.168.122.2
          # Backup and WAL archiving using the streaming protocol
          barman_backup_method: postgres
          # VIP of the primary node. Assuming this VIP address is already
          # present on the system.
          barman_primary_vip: 192.168.122.222
    standby:
      hosts:
        pg2:
          ansible_host: 192.168.122.4
          private_ip: 192.168.122.4
          upstream_node_private_ip: 192.168.122.3
          # Enable barman
          barman: true
          # Private IP address of the barman server
          barman_server_private_ip: 192.168.122.2
          # Backup and WAL archiving using the streaming protocol
          barman_backup_method: postgres
          # VIP of the primary node. Assuming this VIP address is already
          # present on the system.
          barman_primary_vip: 192.168.122.222
          # We don't want to create barman configuration and backup for this
          # instance.
          barman_no_configuration: true
```

### How to include the `setup_barman` role in your Playbook

Below is an example of how to include the `setup_barman` role:

```yaml
---
- hosts: primary, standby
  name: Configure Barman backup on Postgres nodes
  become: true
  gather_facts: true

  collections:
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

  roles:
    - setup_barman
      when: "'setup_barman' in lookup('hypersql_devops.postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/setup_barman/defaults/main.yml](./defaults/main.yml)

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


## Database engines supported
### Supported OS
- CentOS7
- CentOS8

### Supported PostgreSQL Version
- 14.0 - 14.6

## Barman supported
- 3.2.0

## License

BSD

## Author information

Author:

- Cédric Villemain
- Julien Tachoires
- Vibhor Kumar (Reviewer)
- EDB Postgres
- edb-devops@enterprisedb.com www.enterprisedb.com
