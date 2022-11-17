# install_dbserver

This Ansible role installs PostgreSQL or EnterpriseDB Postgresql Advanced
Server versions: 10, 11, 12, 13 or 14 on machines previously configured. 

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the
[Database engines supported](#database-engines-supported) section.

**Note:**
This role does not configure PostgreSQL nor EnterpriseDB Postgres Advanced
Server for replication it only installs PostgreSQL or EnterpriseDB Postgres
Advanced Server binaries across multiple nodes.
Should there be a need to configure a PostgreSQL or EnterpriseDB Postgres
Advanced Server Cluster for replication you can utilize the `setup_replication`
role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

  1. Ansible
  2. `community.general` Ansible Module - Utilized when creating aditional
     users during a Postgres Install
  3. `edb_devops.postgres` -> `setup_repo` role for setting the repository on
     the systems

## Role variables

When executing the role via ansible these are the required variables:

  * **pg_version**

  Postgres Versions supported are: `10`, `11`, `12`, `13` and `14`

  * **pg_type**

  Database Engine supported are: `PG` and `EPAS`

These and other variables can be assigned in the `pre_tasks` definition of the
section: [How to include the install_dbserver role in your Playbook](#how-to-include-the-install_dbserver-role-in-your-playbook)

The rest of the variables can be configured and are available in the:

  * [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `install_dbserver` role does not have any dependencies on any other roles.

## Example Playbook

### Example of inventory file

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pemserver:
      hosts:
        pemserver1:
          ansible_host: 110.0.0.4
          private_ip: 10.0.0.4
    primary:
      hosts:
        primary1:
          ansible_host: 110.0.0.1
          private_ip: 10.0.0.1
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
    standby:
      hosts:
        standby1:
          ansible_host: 110.0.0.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
        standby2:
          ansible_host: 110.0.0.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
          pem_agent: true
          pem_server_private_ip: 10.0.0.4
```

Note: don't forget to replace IP addresses.

### How to include the `install_dbserver` role in your Playbook

Below is an example of how to include the `install_dbserver` role:

```yaml
---
- hosts: primary,standby,pemserver
  name: Install Postgres binaries
  become: yes
  gather_facts: yes

  collections:
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"

  roles:
    - install_dbserver
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

## Database engines supported

### PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
### EnterpriseDB Postgres Advanced Server

| Distribution                      |               10 |               11 |               12 |               13 |               14 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |               :x:|               :x:|               :x:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported

## Playbook execution examples

```bash
# To deploy PostgreSQL version 14
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=PG pg_version=14"
```

```bash
# To deploy EPAS version14
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=EPAS pg_version=14"
```

## License

BSD

## Author information

Author:
  * Doug Ortiz
  * Vibhor Kumar (Co-Author)
  * Julien Tachoires (Co-Author)

Contact: **edb-devops@enterprisedb.com**
