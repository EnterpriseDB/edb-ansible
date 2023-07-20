# execute_binary_upgrade

This role is for performing a major version upgrade on an existing postgres cluster. 
The `pg_upgrade` command is used to perform cluster upgrade. Currently, only primary 
and standby nodes are supported.

## Requirements

In addition to an existing postgres cluster, the following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

### `use_link_method`

When `use_link_method: true`, pg_upgrade will use the link method to perform the upgrade. 
This method creates a hard link between the old cluster data files and the new cluster data files 
instead of the default `copy` method, which copies the data into the new cluster.  
It can be faster than copying each data file, but if pg_upgrade is unsuccessful while using link method, 
the old cluster cannot be restarted.
See [here for more information](https://www.postgresql.org/docs/current/pgupgrade.html) on selecting upgrade method.
Default: `false`

Example:
```yaml
use_link_method: true
```

### `delete_old_cluster`

When `default_old_cluster: true`, the old cluster data and configuration files will be removed.
Default: `false`

Example:
```yaml
delete_old_cluster: true
```

### `old_pg_version`

Version of cluster you are upgrading. 

Example:
```yaml
old_pg_version: 13
```

### `new_pg_version`

Version of cluster you are upgrading to 
Example:
```yaml
new_pg_version: 15
```

### `pg_upgrade_additional_params`

Additional parameters to be passed into the `pg_upgrade` command. 

Example:
```yaml
pg_upgrade_additional_params: '--verbose --quiet'
```

### `pg_init_conf_params`

Additional parameters to be included in the initial configuration of the new cluster. 

Example:
```yaml
pg_init_conf_params:
  - name: wal_level
    value: "replica"
```

### `use_replication_slots`

If using link method, replication slots are not preserved and must be recreated. 
Setting to `true` recreates the replication slots. Default: `true`

Example:
```yaml
use_replication_slots: true
```

### `old_pg_bin_path`

Executable path of old cluster. 

Example:
```yaml
old_pg_bin_path: '/usr/pgsql-13/bin'
```

### `new_pg_bin_path`

Executable path of old cluster. 

Example:
```yaml
new_pg_bin_path: '/usr/pgsql-15/bin'
```

### `old_pg_port`

Listening port of old cluster.

Example:
```yaml
old_pg_port: 5432
```

### `new_pg_port`

Listening port of old cluster.

Example:
```yaml
new_pg_port: 5444
```

### `old_pg_service`

Systemd service name of old cluster service.

Example:
```yaml
old_pg_service: "postgresql-13"
```

### `new_pg_service`

Systemd service name of old cluster service.

Example:
```yaml
new_pg_service: "postgresql-15"
```

### `old_pg_data`

`PGDATA` configured file path for old cluster.

Example:
```yaml
old_pg_data: '/var/lib/pgsql/13/main/data'
```

### `new_pg_data`

`PGDATA` configured file path for new cluster.

Example:
```yaml
new_pg_data: '/var/lib/pgsql/15/main/data'
```

### `base_pg_data`

Base directory used during rsync command, which is only run when using link method. 
Must be above both the old and new cluster data directories.

Example:
```yaml
base_pg_data: '/var/lib/pgsql'
```

### `old_pg_config_dir`

On Debian systems, the configuration files are not stored within the data directory.
This is the configuration directory for the old cluster.

Example:
```yaml
old_pg_config_dir: '/etc/postgresql/13-main'
```

### `new_pg_config_dir`

On Debian systems, the configuration files are not stored within the data directory.
This is the configuration directory for the new cluster.

Example:
```yaml
new_pg_config_dir: '/etc/postgresql/15-main'
```

### `base_pg_config`

Base directory used during rsync command, which is only run when using link method. 
Must be above both the old and new cluster configuration directories. 

Example:
```yaml
base_pg_config: '/etc/postgresql'
```

### `old_pg_wal`

Wal file directory for old cluster.
If `pg_wal` directory is within the `pg_data` directory, no input is required.
If not listed and not within `pg_data`, the wal files will not be preserved.
Only needed if using link mode. 

Example:
```yaml
old_pg_wal: '/var/lib/pgsql/13/main/data/pg_wal'
```

### `new_pg_wal`

Wal file directory for new cluster. This directory is used while initializing the new cluster. 

Example:
```yaml
new_pg_wal: '/var/lib/pgsql/14/main/data/pg_wal'
```

### `base_pg_wal`

Base directory used during rsync command, which only runs if using link method. 
Must be above both the old and new cluster wal directories. 

Example:
```yaml
base_pg_wal: '/var/lib/pgsql/15/main/data'
```

### `new_pg_tblspc`

Directory to place tablespaces of the new cluster.

Example:
```yaml
new_pg_tblspc: '/var/lib/pgsql/15/main/data/pg_tblspc'
```

### `pg_database`

Name of the postgres database. Default: `postgres`

Example:
```yaml
pg_database: "postgres"
```

## Dependencies

This role does not have any dependencies, but packages repositories should have
been configured beforehand with the `setup_repo` role.

## Example Playbook

### Hosts file content

This role supports nodes in the primary and standby groups. Any additional cluster nodes will not be upgraded.

Content of the `inventory.yml` file:
```yaml
---
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
          replication_type: asynchronous
```

### How to include the `execute_binary_upgrade` role in your Playbook

Below is an example of how to include the `execute_binary_upgrade` role:
```yaml
---
- hosts: primary,standby
  name: Perform a major version upgrade
  become: true
  gather_facts: yes
  any_errors_fatal: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        old_pg_version: 13
        new_pg_version: 15
        use_link_method: false
        delete_old_cluster: true
        
        pg_type: "PG"

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: execute_binary_upgrade
      when: "'execute_binary_upgrade' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/execute_binary_upgrade/defaults/main.yml](./defaults/main.yml)
  * [roles/execute_binary_upgrade/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/execute_binary_upgrade/vars/PG_Debian.yml](./vars/PG_Debian.yml)
  * [roles/execute_binary_upgrade/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/execute_binary_upgrade/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)

## License

BSD

## Author information

Author:

  * Hannah Stoik
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
