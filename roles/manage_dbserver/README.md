Role Name
=========

manage_dbserver role is for managing the database cluster. It makes the managing of the database cluster by giving key tasks. In all the roles, we have used the tasks given in the this role.

Requirements
------------

Following are the dependencies and requirement of this role. 
1. Ansible
2. community.general Ansible Module - Utilized when creating aditional users during a Postgres Install


Role Variables
--------------

This role allows users to pass following variables which helps managing day to day tasks:
1. pg_postgres_conf_params: Using this parameters user can set the database parameters
 
Example:
 
```  
pg_postgres_conf_params: ""
  - name: listen_addresses
    value: "*"

pg_hba_ip_addresses: 
  - contype: "host"
    users: "all"
    databases: "all"
    method: "scram-sha-256"
    source: "127.0.0.1/32"
    state: present

pg_slots: ""
  - name: "physcial_slot"
    slot_type: "physical"
    state: present
  - name: "logical_slot"
    slot_type: "logical"
    output_plugin: "test_decoding"
    state: present
    database: "edb"

pg_extensions: ""
    - name: "postgis"
      database: "edb"
      state: present

pg_grant_privileges:
    - roles: "efm_user"
      database: "edb"
      privileges: execute
      schema: pg_catalog
      objects: pg_current_wal_lsn(),pg_last_wal_replay_lsn(),pg_wal_replay_resume(),pg_wal_replay_pause()
      type: function

pg_grant_roles:
    - role: pg_monitor
      user: enterprisedb

pg_sql_scripts:
    - file_path: "/usr/edb/as12/share/edb-sample.sql"
      db: edb
      
pg_copy_files: ""
    - file: "./test.sh"
      remote_file: "/var/lib/edb/test.sh"
      owner: efm
      group: efm
      mode: 0700

pg_query: ""
    - query: "Update test set a=b"
      db: edb 

pg_pgpass_values: ""
    - host: "127.0.0.1"
      database: edb
      user: enterprisedb
      password: <password>
      state: present

pg_databases: ""
    - name: edb_gis
      owner: edb
      encoding: UTF-8
```

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:


Hosts file content
----------------

Content of the hosts.yml file:



      servers:
        main1:
          node_type: primary
          public_ip: xxx.xxx.xxx.xxx
        standby11:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
        standby12:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx

How to include the 'manage_dbserver' role in your Playbook
----------------

Below is an example of how to include the init_dbserver role:



    - hosts: localhost
      name: Install EFM on Instances
      #connection: local
      become: true
      gather_facts: no

      collections:
        - edb_devops.postgres

      vars_files:
        - hosts.yml

      pre_tasks:
        # Define or re-define any variables previously assigned
        - name: Initialize the user defined variables
          set_fact:
            os: "CentOS7"
            pg_type: "EPAS"
            pg_version: 12
            pg_data: "/data/pgdata"
            pg_postgres_conf_params: ""
              - name: listen_addresses
                value: "*"

            pg_hba_ip_addresses:
              - contype: "host"
                users: "all"
                databases: "all"
                method: "scram-sha-256"
                source: "127.0.0.1/32"
                state: present

            pg_slots:
              - name: "physcial_slot"
                slot_type: "physical"
                state: present
              - name: "logical_slot"
                slot_type: "logical"
                output_plugin: "test_decoding"
                state: present
                database: "edb"

      roles:
         - manage_dbserver

License
-------

BSD
