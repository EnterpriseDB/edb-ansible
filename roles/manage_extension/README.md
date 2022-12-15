# manage_extension

This Ansible Role install and manage PostgreSQL Extension

## Requirements

1. Ansible
2. `hypersql_devops.postgres` -> `setup_repo` - for Installing the PG repository

## Role variables

When executing the role via Ansible these are required variables:

- **pg_version**

    Postgres Version supported are: `14.0`, `14.1`, `14.2`, `14.3`, `14.3`, `14.5`, `14.6`

- **pg_type**
    
    Database Engine supported are: `PG`

- **pg_extension_list**

    Extension supported are: `potgis`, `pgaudit`

Example:

```yaml
# install only postgis
pg_extension_list:
    - postgis
```

The rest of the variables can be configured and are available in the:

- [roles/manage_extension/defaults/main.yml](./defaults/main.yml)
- [roles/manage_extension/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
- [roles/manage_extension/vars/PG_Debian.yml](./vars/PG_Debian.yml)


## Dependencies

This role depends on the `common` role.

## Example Playbook

### Example of inventory file

Content of the `inventory.yml` file:

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


### How to include the `manage_extension` role in your Playbook

Below is an example of how to include the `manage_extension` role for
installing extension :

```yaml
---
- hosts: all
  name: Install Extension
  become: yes
  gather_facts: yes

  collections:
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

        pg_extension_list:
            - postgis
            - pgaudit

  roles:
    - manage_extension
```

## Database engines supported

### Community PostgreSQL

| Distribution                      |               14 |
| --------------------------------- |:----------------:|
| CentOS 7                          |:white_check_mark:|
| CentOS 8                          |:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported

## PostgreSQL extension supported

| PostgreSQL Engine      |     postgis |
| ---------------------- |:-----------:|
| RedHat - PG v14        |          3.2|

| PostgreSQL Engine      |     pgaudit |
| ---------------------- |:-----------:|
| Debian - PG v14        |          1.6|

## Playbook execution examples
```bash
# To deploy community Postgres version 14.6 on CentOS8 hosts with the user centos
$ ansible-playbook playbook.yml \
  -u centos \
  -i inventory.yml \
  --extra-vars="pg_version=14.6 pg_type=PG"
```

## License

BSD

## Author information
Author:
  * [Sang Myeung Lee](https://github.com/sungmu1)
