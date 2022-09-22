# setup_pgbackrestserver

This role is for setting up pgBackRest server. pgBackRest is a backup and recovery tool for Postgres.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

### `pgbackrest_user`

System user running pgBackRest commands. Default: `pgbackrest`

Example:
```yaml
pgbackrest_user: 'pgbackrest'
```

### `pgbackrest_group`

System group the pgbackrest user is part of. Default: `pgbackrest`

Example:
```yaml
pgbackrest_group: 'pgbackrest'
```

### `pgbackrest_configuration_file`

pgBackRest main configuration file path. Default: `/etc/pgbackrest.conf`

Example:
```yaml
pgbackrest_configuration_file: '/etc/pgbackrest.conf'
```

### `pgbackrest_lock_path`

Path of the pgBackRest lock directory. Default: `/var/run/pgbackrest`

Example:
```yaml
pgbackrest_lock_path: '/var/run/pgbackrest'
```

### `pgbackrest_home`

Path of the pgbackrest home directory. Backup files and archived WAL files are stored in this root directory. Default: `/var/lib/pgbackrest`

Example:
```yaml
pgbackrest_home: '/var/lib/pgbackrest'
```

### `pgbackrest_log_file`

pgBackRest logging file path. Default: `/var/log/pgbackrest/pgbackrest.log`

Example:
```yaml
pgbackrest_log_file: '/var/log/pgbackrest/pgbackrest.log'
```

### `pgbackrest_log_level_console`

Logging level for console logging. Could be `off`, `error`, `warn`, `info`, `detail`, `debug` or `trace`. 
Default: `info`

Example:
```yaml
pgbackrest_log_level_console: 'info'
```

### `pgbackrest_log_level_file`

Logging level for file logging. Could be `off`, `error`, `warn`, `info`, `detail`, `debug` or `trace`. 
Default: `debug`

Example:
```yaml
pgbackrest_log_level_file: 'debug'
```

### `archive_repo_directory`

Path of the pgBackRest archive repository. Backup files and archived WAL files are stored in this directory. 
Default: `/var/lib/pgbackrest/backups`

Example:
```yaml
archive_repo_directory: '/var/lib/pgbackrest/backups'
```

### `repo_retention_full_type`

Retention type for full backups. Determines if the value set in `repo_retention_full` represents a time period (days) 
or number of full backups to keep. Could be `count` or `time`. Default: `count`

Example:
```yaml
repo_retention_full_type: "count"
```

### `repo_retention_full`

Number of full backups to keep. Default: `2`

Example:
```yaml
repo_retention_full: 2
```

### `repo_cipher_type`

Cipher to encrypt the repository. Could be `none` or `aes-256-cbc`. Default: `aes-256-cbc`

Example:
```yaml
repo_cipher_type: 'aes-256-cbc'
```

### `backup_standby`

Perform backups on a standby instead of the primary. Both primary and standby databases are required to perform a backup, 
although a majority of the files will be copied from the standby to reduce load on the primary. Default: `n`

Example:
```yaml
backup_standby: "y"
```

### `process_max`

Number of parallel processes used during backup and recovery. Setting too high may impact database performance. Default: `1`

Example:
```yaml
process_max: 1
```

### `delta`

Restore or backup using checksums instead of timestamps. During a restore, the cluster data are expected to be 
present but empty. If they are not empty, the restore will fail. Setting `delta:y` will have pgBackRest automatically 
determine which files in database cluster directory need to be restored and which can be preserved. It will remove any 
unrecognized files to avoid divergent changes. 
Default: `n`

Example:
```yaml
delta: "y"
```

### `primary_pgbr_config_file`

File path of pgBackRest main configuration file on all other nodes running pgBackRest. Default: `/etc/pgbackrest.conf` 

Example:
```yaml
primary_pgbr_config_file: '/etc/pgbackrest.conf'
```

### `pg_instance_name`

Name of the postgres instance running on primary node. Default: `main`

Example:
```yaml
pg_instance_name: 'main'
```

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
    pgbackrest:
      hosts:
        pgbackrest1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
```

### How to include the `setup_pgbackrestserver` role in your Playbook

Below is an example of how to include the `setup_pgbackrestserver` role:

```yaml
---
- hosts: pgbackrest
  name: Deploy pgbackrest servers
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres
  
  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"

  roles:
    - setup_repo
    - setup_pgbackrestserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All of the variables are available at:

* [/roles/setup_pgbackrestserver/defaults/main.yml](./defaults/main.yml)

## License

BSD

## Author information

Author:

  * Hannah Stoik
  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com