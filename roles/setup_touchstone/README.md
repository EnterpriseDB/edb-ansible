# setup_touchstone

This role is for setting up additional packages and software for characterizing
system performance.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

The variables that can be configured and are available in the:

  * [roles/setup_touchstone/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `touchstone_version`

The version of Touchstone.  Default: 0.2.0

Example:
```yaml
touchstone_version: 0.2.0
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
