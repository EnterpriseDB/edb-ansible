# init_dbserver

This Ansible Galaxy Role Initializes Postgres versions: 14 on instances previously configured.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: _Database engines supported_ section.

**Note:**
The role does not configure Postgresfor replication it only installs 
Postgres across multiple nodes: Main and Standby.
Should there be a need to configure a Postgres Cluster for replication you can utilize the `setup_replication` role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

1. Ansible
2. `community.general` Ansible Module - Utilized when creating aditional
   users during a Postgres Install. Only on primary nodes.
3. `hypersql_devops.postgres` -> `setup_repo` - for repository installation
4. `hypersql_devops.postgres` -> `install_dbserver` - for installation of
   PostgreSQL binaries.

## Role variables

When executing the role via ansible there are three required variables:

- **_pg_version_**

<<<<<<< Updated upstream
  Postgres Versions supported are: `14.0`,`14.1`,`14.2`,`14.3`,`14.3`,`14.5`,`14.6`
=======
  Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`
>>>>>>> Stashed changes

- **_pg_type_**

Database Engine supported are: `PG`

These and other variables can be assigned in the `pre_tasks` definition of the
section: _How to include the `init_dbserver` role in your Playbook_

This role allows users to pass following variables which helps managing day to
day tasks:

### `pg_data`

Using this parameters user can set the database cluster directory path.

Example:

```yaml
pg_data: "/var/lib/pgsql/14/data"
```

### `pg_wal`

Using this parameters user can set the database wal directory path.

Example:

```yaml
pg_wal: "/var/lib/pgsql/14/pg_wal"
```

### `pg_log`

Using this parameters user can set the database log directory path.

Example:

```yaml
pg_log: "/var/run/pg_log"
```

### `pg_local_wal_archive_dir`

Using this parameters user can set the database log directory path.

Example:

```yaml
pg_local_wal_archive_dir: "/var/lib/pgsql/14/archive"
```

The rest of the variables can be configured and are available in the:

- [roles/init_dbserver/vars/PG_Debian.yml](./vars/PG_Debian.yml)
- [roles/init_dbserver/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)

## Dependencies

The `init_dbserver` role does not have any dependencies on any other roles.

## Example Playbook

### Inventory file content

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
          replication_type: synchronous
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
```

### How to include the `init_dbserver` role in your Playbook

Below is an example of how to include the `init_dbserver` role:

```yaml
---
- hosts: primary,pemserver
  name: Initialize Postgres instances
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
    - initdb_dbserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/init_dbserver/defaults/main.yml](./defaults/main.yml)
- [roles/init_dbserver/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
- [roles/init_dbserver/vars/PG_Debian.yml](./vars/PG_Debian.yml)
<<<<<<< Updated upstream
- [roles/init_dbserver/vars/edb-ssl.yml](./vars/ssl.yml)
=======
- [roles/init_dbserver/vars/ssl.yml](./vars/ssl.yml)
>>>>>>> Stashed changes

## Database engines supported

### PostgreSQL

| Distribution                      |               14 |
| --------------------------------- |:----------------:|
| CentOS 7                          |:white_check_mark:|
| CentOS 8                          |:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|

- :white_check_mark: - Tested and supported

## Playbook execution examples

```bash
# To deploy community Postgres version 14 with the user centos
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --extra-vars="pg_version=14.6 pg_type=PG"
```

## License

BSD

## Author information

Author:
  * [Sang Myeung Lee](https://github.com/sungmu1)

Original Author:

- Doug Ortiz
- Julien Tachoires
- Vibhor Kumar
- EDB Postgres
- DevOps
- edb-devops@enterprisedb www.enterprisedb.com
