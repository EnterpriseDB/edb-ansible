# setup_touchstone_tools

This role is for setting up additional packages and software for characterizing
system performance using sar, pidstat, readprofile, oprofile or perf.

See project homepage for more details, in particular the man pages which are
human readable: https://gitlab.com/touchstone/touchstone-tools

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.

## Role Variables

The variables that can be configured and are available in the:

  * [roles/setup_touchstone_tools/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `touchstone_tools_version`

The version of Touchstone Tools.  Default: 0.6.1

Example:
```yaml
touchstone_version: 0.6.1
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
