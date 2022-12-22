# setup_barmanserver

This role is for setting up Barman server. Barman is a backup and recovery tool
for Postgres.

## Requirements

Following are the requirements of this role.

1. Ansible
2. `hypersql_devops.postgres` -> `setup_repo` role for setting the repository on
   the systems.

## Role Variables

### `barman_user`

System user running barman commands. Default: `barman`

Example:

```yaml
barman_user: "barman"
```

### `barman_group`

System group the barman user is part of. Default: `barman`

Example:

```yaml
barman_group: "barman"
```

### `barman_configuration_file`

Barman main configuration file path. Default: `/etc/barman.conf`

Example:

```yaml
barman_configuration_file: "/etc/barman.conf"
```

### `barman_configuration_files_directory`

Directory containing the included barman configuration files.
Default: `/etc/barman.d`

Example:

```yaml
barman_configuration_files_directory: "/etc/barman.d"
```

### `barman_home`

Path of the barman home directory. Backup files and archived WAL files are
stored in this root directory. Default: `/var/lib/barman`

Example:

```yaml
barman_home: "/var/lib/barman"
```

### `barman_lock_directory`

Path of the barman execution directory. Default: `/var/run/barman`

Example:

```yaml
barman_lock_directory: "/var/run/barman"
```

### `barman_log_file`

Barman logging file path. Default: `/var/log/barman/barman.log`

Example:

```yaml
barman_log_file: "/var/log/barman/barman.log"
```

### `barman_log_level`

Logging level.

- Options: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Default: `INFO`

Example:

```yaml
barman_log_level: "INFO"
```

### `barman_compression`

Compression tool to use for backups and archived WAL files.

- Options: gzip, lz4, zstd, none
- Default: `gzip`

Example:

```yaml
barman_compression: "gzip"
```

## Dependencies

- setup_repo: packages repositories should have been configured beforehand with the `setup_repo` role.
- install_dbserver: Postgres binaries are required for Barman

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
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

  roles:
    - setup_repo
    - install_dbserver
    - setup_barmanserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/setup_barmanserver/defaults/main.yml](./defaults/main.yml)

## License

BSD

## Author information

Author:

- [Sung Woo Chang](https://github.com/dbxpert)

Original Authors:

- Julien Tachoires
- Vibhor Kumar (Reviewer)
- EDB Postgres
- edb-devops@enterprisedb.com www.enterprisedb.com
