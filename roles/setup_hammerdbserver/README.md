
# setup_hammerdbserver

This role is for setting up a server for [HammerDB](https://hammerdb.com/).
HammerDB is the leading benchmarking and load testing software for the worlds
most popular databases.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository
     on the systems.

## Role Variables

The variables that can be configured and are available in the:

  * [roles/setup_hammerdbserver/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `hammerdb_version`

The release version of HammerDB.  Default: 3.3

Example:
```yaml
hammerdb_version: 3.3
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
