manage_dbpatches
=========

This role helps in applying patches on EDB failover manager cluster based on physical streaming replication. The role tries to apply patches first on the standby(s) and last it applies to primary. It gives a user choice to apply patches on all standby(s) in parallel or in one at a time.


Requirements
------------

Following are the dependencies and requirement of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_efm` - role for setting up failover manager cluster
     on the systems.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

When executing the role via ansible these are the required variables:

  * ***os***

    Operating Systems supported are: CentOS7, CentOS8, RHEL7, RHEL8, Rocky8, AlmaLinux8, Debian10 and Ubuntu20

The rest of the variables can be configured and are available in the:

  * [roles/manage_dbpatches/defaults/main.yml](./defaults/main.yml)
  * [roles/manage_dbpatches/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/manage_dbpatches/vars/PG_Debian.yml](./vars/PG_Debian.yml)
  * [roles/manage_dbpatches/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/manage_dbpatches/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)

Below is the documentation of the rest of the variables:

### `pg_package_list`

Using this variable a user can mention which patches need to applied on database servers of the failover cluster.

Example:
```yaml
pg_package_list:
  - edb-as14-server*
  - edb-efm44*
```

### `user_package_list`

Using this variable a user can mention which patches need to applied on all servers of the failover cluster.

Example:
```yaml
user_package_list:
  - openjdk-8-jdk
```

### `user_defined_services`

Using this variable a user can mention all the services (s)he wants to stop before applying the patches and start after applying the patches.

Example:
```yaml
user_defined_services:
  - pemagent
```

### `run_in_sequence`

Using this variable a user can specify whether they want to apply patches one standby at a time or in parallel.
Default: `false`

Example:
```yaml
run_in_sequence: false
```


Example Playbook
----------------

### Inventory file content

Following is an inventory example for using this role
Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:
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

Below is an example of how to include the `manage_dbpatches` role:

```yaml
---
- hosts: primary,pemserver
  name: Apply database patches
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"
        pg_package_list:
            - edb-as14-server*
            - edb-efm44*
        user_package_list:
            - edb-efm44*

  roles:
    - role: manage_dbpatches
      when: "'manage_dbpatches' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```
License
-------

BSD

## Author information

Author:

  * Doug Ortiz
  * Julien Tachoires
  * Vibhor Kumar
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
