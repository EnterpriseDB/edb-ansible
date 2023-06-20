# manage_touchstone_tools

`manage_touchstone_tools` role is for managing the use of the touchstone system performance 
tools. For more information on the touchstone-tools, visit the project homepage:
https://gitlab.com/touchstone/touchstone-tools.

There are eight tasks that this role can perform:
  1. [Start collecting system stats](#startsystemstats)
  2. [Stop collecting system stats](#stopsystemstats)
  3. [Start collecting database stats](#startdbstats)
  4. [Stop collecting database stats](#stopdbstats)
  5. [Process pidstat data](#processpidstatdata)
  6. [Plot sar data](#plotsardata)
  7. [Plot pidstat data](#plotpidstatdata)
  8. [Plot database data](#plotdbdata)

## Requirements

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.
  3. `edb_devops.edb_postgres` -> `setup_touchstone_tools` role for installing the touchstone appimage.

## Role Variables

The variables that can be configured and are available in the:

  * [roles/manage_touchstone_tools/defaults/main.yml](./defaults/main.yml)

Each task within this role has a different set of required variables. 
Below is the documentation for each of those tasks and their variables'.

### `start_system_stats`

This task starts the collection of system statistics.

#### `ts_output_dir`

The output directory for the touchstone-tools data collection. This must be a 
directory that does not already exist.

#### `sec_bw_sample`

The number of seconds between samples, default 60.
 
#### How to include `start_system_stats` in your playbook

Below is an example of how to put `start_system_stats` in your playbook.

```yaml
- name: Include start_system_stats tasks to start sysstat data collection
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: start_system_stats
  vars:
    ts_output_dir: "/var/log/touchstone/system_stats"
    sec_bw_sample: 30
```

### `stop_system_stats`

This task stops the collection of system statistics.

#### `ts_output_dir`

The output directory for the touchstone-tools data collection. This must be a 
directory that does not already exist.
 
#### How to include `stop_system_stats` in your playbook

Below is an example of how to put `stop_system_stats` in your playbook.

```yaml
- name: Include stop_system_stats tasks to stop sysstat data collection
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: stop_system_stats
  vars:
    ts_output_dir: "/var/log/touchstone/system_stats"
```

### `start_db_stats`

This task starts the collection of database statistics.

#### `ts_output_dir`

The output directory for the touchstone-tools database data collection.

#### `sec_bw_sample`

The number of seconds between samples, default 60.

#### `pg_database`

The database name to connect to.

#### `pg_server_hostname`

Database server host or docker directory. Same as `-h` in `psql` commands.

#### `pg_port`

The database server port. Same as `-p` in `psql` commands.

#### `pg_owner`

Database connections username. Same as `-U` in `psql` commands.
 
#### How to include `start_db_stats` in your playbook

Below is an example of how to put `start_db_stats` in your playbook.

```yaml
# if vars pg_database, pg_port, pg_owner are already set by ansible, they are not required to be passed in
- name: Include start_db_stats tasks to start pgsql stats data collection
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: start_db_stats
  vars:
    ts_output_dir: "/var/log/touchstone/db_stats"
    sec_bw_sample: 15
    pg_database: "postgres"
    pg_server_hostname: "primary1"
    pg_port: 5432
    pg_owner: "postgres"
```

### `stop_db_stats`

This task stops the collection of database statistics.

#### `ts_output_dir`

The output directory for the touchstone-tools database data collection.
 
#### How to include `stop_db_stats` in your playbook

Below is an example of how to put `stop_db_stats` in your playbook.

```yaml
- name: Include stop_db_stats tasks to stop pgsql stats data collection
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: stop_db_stats
  vars:
    ts_output_dir: "/var/log/touchstone/db_stats"
```

### `process_pidstat_data`

This task processes the `pidstat.txt` file generated during system stat collection.
This task generates the `pidstat.csv` file and places in the same directory as the `pidstat.txt`.

#### `pidstat_txt_file`

The file location of the `pidstat.txt`. This file is generated during sysstat collection.
Usually placed within the `ts_output_file` directory used during `stop_system_stats`.
If not specified, it will use the `ts_output_file` directory to generate, but this may not be an accurate location. 
 
#### How to include `process_pidstat_data` in your playbook

Below is an example of how to put `process_pidstat_data` in your playbook.

```yaml
- name: Include process_pidstat_data tasks to start sysstat data collection
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: process_pidstat_data
  vars:
    pidstat_txt_file: "/var/log/touchstone/system_stats/pidstat.txt"
```

### `plot_sar_data`

This task plots the generated sar data.

#### `ts_output_dir`

The directory of the ts-sysstat processed sar data. This location is the 
output directory (`ts_output_dir`) from the `stop_system_stats` tasks. 

#### `ts_plot_output_dir`

The directory for the generated plots to be placed. Plotting the sar data will generate 
new directories within this directory. Defaults to `ts_output_dir` if not value specified.

#### `plot_size`

The dimensions of the generated plots. Default `1600,1000`.

#### How to include `plot_sar_data` in your playbook

Below is an example of how to put `plot_sar_data` in your playbook.

```yaml
- name: Include plot_sar_data tasks to plot sar data
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: plot_sar_data
  vars:
    ts_output_dir: "/var/log/touchstone/system_stats"
    ts_plot_output_dir: "/var/log/touchstone/system_stats"
    plot_size: "800,500"
```

### `plot_pidstat_data`

This task plots the generated and processed pidstat data in `pidstat.csv`.

#### `pidstat_csv_file`

The location of the processed `pidstat.csv` file.

#### `ts_plot_output_dir`

The directory for the generated plots to be placed. 

#### `plot_size`

The dimensions of the generated plots. Default `1600,1000`.

#### How to include `plot_pidstat_data` in your playbook

Below is an example of how to put `plot_pidstat_data` in your playbook.

```yaml
- name: Include plot_pidstat_data tasks to plot pidstat data
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: plot_pidstat_data
  vars:
    pidstat_csv_file: "/var/log/touchstone/system_stats/pidstat.csv"
    ts_plot_output_dir: "/var/log/touchstone/system_stats/pidstat_plots"
    plot_size: "1600,1000"
```

### `plot_db_data`

This task plots the generated database stats.

#### `pg_databse`

The database name to plot the stats from.

#### `ts_output_dir`

The directory of the ts-pgsql-stat collected data. This location is the 
output directory (`ts_output_dir`) from the `stop_db_stats` tasks. 

#### `ts_plot_output_dir`

The directory for the generated plots to be placed. 
Defaults to `ts_output_dir` if not value specified.

#### `plot_size`

The dimensions of the generated plots. Default `1600,1000`.

#### How to include `plot_db_data` in your playbook

Below is an example of how to put `plot_db_data` in your playbook.

```yaml
- name: Include plot_db_data tasks to plot pgsql data
  ansible.builtin.include_role:
    name: manage_touchstone_tools
    tasks_from: plot_db_data
  vars:
    pg_database: "postgres"
    ts_output_dir: "/var/log/touchstone/db_stats"
    ts_plot_output_dir: "/var/log/touchstone/db_stats/pgsql_plots"
    plot_size: "800,500"
```

## License

BSD

## Author information

Author:
  * Hannah Stoik
  * Mark Wong
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com