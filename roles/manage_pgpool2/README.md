# manage_pgpool2

This role is for managing PgpoolII configuration parameters and user list.

## Requirements

Following are the dependencies and requirement of this role.
  1. Ansible
  2. `edb_devops.postgres` -> `setup_pgpool2` - role for setting up PgpoolII
     on the systems.

## Role Variables

When executing the role via ansible these are the required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12 and 13

  * ***pg_type***

  Database Engine supported are: PG and EPAS


The rest of the variables can be configured and are available in the:

  * [roles/manage_pgpool2/vars/PG.yml](./vars/PG.yml)
  * [roles/manage_pgpool2/vars/EPAS.yml](./vars/EPAS.yml)

Below is the documentation of the rest of the variables:

### pgpool2_configuration

This is the list of the configuration parameters to be changed in PgpoolII
configuration file.

Example:
```yaml
pgpool2_configuration:
  - key: "port"
    value: 6432
    state: present
  - key: "socket"
    value: "/tmp"
    # Add quotes around the value
    quoted: true
    state: present
  - key: "ssl_ca_cert"
    state: absent
```

Note: The PgpoolII parameters taking a string value must be quoted in the
configuration file, this behavior can be achieved by setting to `quoted`
attribute to `true`. Default value is `false`.

The `state` attribute defines if the parameter must be present or not in the
configuration file. Default value is `present`.

### pgpool2_users

This is the list of PgpoolII user account to managed.

Example:
```yaml
pgpool2_users:
  - name: "my_user1"
    pass: "password"
    auth: scram
  - name: "my_user2"
    pass: "password"
    auth: md5
  - name: "my_user_to_be_removed"
    state: absent
```

Two authentication methods are supported: `scram` and `md5`.

The `state` attribute defines if the user must be present or not in the
authentication file. Default value is `present`.

## Dependencies

This role does not have any dependencies, but a PgpoolII instance should have
been deployed beforehand with the `setup_pgpool2` role.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pgpool2:
      hosts:
        pool1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
```

### User defined variables

Defining variables can be done using a dedicated file and including this file
 at execution time with the `ansible-playbook` CLI option:

   * `--extra-vars=@./vars.yml`

Content example of the `vars.yml` file:

```yaml
---
pg_type: "PG"
pg_version: 13

pgpool2_configuration:
  - key: "port"
    value: 6432
    state: present
  - key: "socket"
    value: "/tmp"
    # Add quotes around the value
    quoted: true
    state: present
  - key: "ssl_ca_cert"
    state: absent

pgpool2_users:
  - name: "my_user1"
    pass: "password"
    auth: scram
  - name: "my_user2"
    pass: "password"
    auth: md5
  - name: "my_user_to_be_removed"
    state: absent
```

### How to include the `manage_pgpool2` role in your Playbook

Below is an example of how to include the `manage_pgpool2` role:
```yaml
---
- hosts: pgpool2
  name: Manage PgpoolII instances
  become: yes
  gather_facts: yes
  roles:
    - manage_pgpool2
```

## License

BSD

## Author information

Author:

  * Julien Tachoires
  * Vibhor Kumar (Reviewer)
  * EDB Postgres
  * julien.tachoires@enterprisedb.com www.enterprisedb.com
