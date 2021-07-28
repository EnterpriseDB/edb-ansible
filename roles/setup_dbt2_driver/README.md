# setup_dbt2_driver

This role is for setting up a driver server for
[DBT-2](http://osdldbt.sourceforge.net/).  DBT-2(TM) is an OLTP transactional
performance test. It simulates a wholesale parts supplier where several workers
access a database, update customer information and check on parts inventories.
DBT-2 is a fair usage implementation of the the TPC's [TPC-C(TM)
Benchmark](http://www.tpc.org/tpcc/) specification. The results of a test run
include transactions per second, CPU utilization, I/O activity, and memory
utilization.

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository
     on the systems.

## Role Variables

The variables that can be configured and are available in the:

  * [roles/setup_dbt2_driver/defaults/main.yml](./defaults/main.yml)

Below is the documentation of the rest of the main variables:

### `dbt2_version`

The release version of DBT-2.  Default: HEAD

Example:
```yaml
dbt2_version: HEAD
```

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
