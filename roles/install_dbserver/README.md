# install_dbserver

This Ansible role installs PostgreSQL versions: 14 on machines previously configured.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the
[Database engines supported](#database-engines-supported) section.

**Note:**
This role does not configure PostgreSQL for replication it only installs PostgreSQL binaries across multiple nodes.
Should there be a need to configure a PostgreSQL Cluster for replication you can utilize the `setup_replication` role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

1. Ansible
2. `community.general` Ansible Module - Utilized when creating aditional
   users during a Postgres Install
3. `tmax_opensql.postgres` -> `setup_repo` role for
   setting the repository on the systems

## Role variables

When executing the role via ansible these are the required variables:

- **pg_version**

  Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`

- **pg_type**

  Database Engine supported are: `PG`

This role allows users to pass following variables which helps managing day to
day tasks:

### `rpm_install`

Using this parameters user can set install with rpm file.

Example:

```yaml
rpm_install: true
```

These and other variables can be assigned in the `pre_tasks` definition of the
section: [How to include the install_dbserver role in your Playbook](#how-to-include-the-install_dbserver-role-in-your-playbook)

The rest of the variables can be configured and are available in the:

- [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `install_dbserver` role does not have any dependencies on any other roles.

## Example Playbook

### Example of inventory file

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: 110.0.0.1
          private_ip: 10.0.0.1
    standby:
      hosts:
        standby1:
          ansible_host: 110.0.0.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
        standby2:
          ansible_host: 110.0.0.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
```

Note: don't forget to replace IP addresses.

### How to include the `install_dbserver` role in your Playbook

Below is an example of how to include the `install_dbserver` role:

```yaml
---
- hosts: primary,standby,pemserver
  name: Install Postgres binaries
  become: true
  gather_facts: true

  collections:
    - tmax_opensql.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

  roles:
    - install_dbserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Database engines supported
### Supported OS
- CentOS7
- CentOS8

### Supported PostgreSQL Version
- 14.0 - 14.6

## Playbook execution examples

```bash
# To deploy PostgreSQL version 14
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=PG pg_version=14.6"
```

## License

BSD

## Author information

Author:

- [Sang Myeung Lee](https://github.com/sungmu1)

Original Author:

- Vibhor Kumar (Co-Author)
- Julien Tachoires (Co-Author)
