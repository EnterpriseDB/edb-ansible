# setup_barmanserver

This role is for setting up Barman server. Barman is a backup and recovery tool
for Postgres.

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
section: *How to include the `setup_barmanserver` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/setup_barmanserver/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `barman_user`

System user running barman commands. Default: `barman`

Example:
```yaml
barman_user: 'barman'
```

### `barman_group`

System group the barman user is part of. Default: `barman`

Example:
```yaml
barman_group: 'barman'
```

### `barman_configuration_file`

Barman main configuration file path. Default: `/etc/barman.conf`

Example:
```yaml
barman_configuration_file: '/etc/barman.conf'
```

### `barman_configuration_files_directory`

Directory containing the included barman configuration files.
Default: `/etc/barman.d`

Example:
```yaml
barman_configuration_files_directory: '/etc/barman.d'
```

### `barman_home`

Path of the barman home directory. Backup files and archived WAL files are
stored in this root directory. Default: `/var/lib/barman`

Example:
```yaml
barman_home: '/var/lib/barman'
```

### `barman_lock_directory`

Path of the barman execution directory. Default: `/var/run/barman`

Example:
```yaml
barman_lock_directory: '/var/run/barman'
```

### `barman_log_file`

Barman logging file path. Default: `/var/log/barman/barman.log`

Example:
```yaml
barman_log_file: '/var/log/barman/barman.log'
```

### `barman_log_level`

Logging level. Default: `INFO`

Example:
```yaml
barman_log_level: 'INFO'
```

### `barman_compression`

Compression tool to use for backups and archived WAL files. Default: `gzip`

Example:
```yaml
barman_compression: 'gzip'
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
    barmanserver:
      hosts:
        barman1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
```

### How to include the `setup_barmanserver` role in your Playbook

Below is an example of how to include the `setup_barmanserver` role:
```yaml
---
- hosts: barmanserver
  name: Deploy Barman Servers
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
    # Install Postgres binaries required for Barman
    - install_dbserver
    - setup_barmanserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_barmanserver/defaults/main.yml](./defaults/main.yml)

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
