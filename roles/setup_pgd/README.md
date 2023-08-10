setup_pgd
=========

This role helps in configuration of PGD Node cluster.

Requirements
------------

Following are the requirements of this role.
  1. Ansible
  2. `edb_devops.edb_postgres` -> `setup_repo` role for setting the repository on
     the systems.
  3. `edb_devops.edb_postgres` -> `install_dbserver` role for installing the necessary packages on at least the lead primary.
  4. `edb_devops.edb_postgres` -> `init_dbserver` role for initializing the database cluster on the lead primary.

Role Variables
--------------

### `edb_enable_tde`

Flag to enable TDE in the cluster. If `true`, then additional TDE variables must be defined.
See `init_dbserver` role for additional TDE variables. Default: `false`.

### `pgd_version`

Version of PGD to install and configure. Default: `5`

### `install_pgd`

Flag for installing PGD packages. Default: `false`.

### `pgd_cluster_database`

Name of the PGD cluster database.

### `pgd_cluster_database_owner`

Username of PGD database owner.

### `pgd_cluster_database_owner_password`

Password for PDG cluster database owner. If none is provided, it will be generated during cluster initialization. 

### `pgd_replication_user`

Username of PGD replication user.

### `pgd_replication_user_password`

Password for PGD replication user. If none is provided, it will be generated during cluster initialization. 

### `pgd_cluster_name`

Name of PGD cluster to be initialized. 

### `pgd_local_node_name`

Hostname of local node.

The rest of the variables can be configured and are available in the:

  * [roles/setup_pgd/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgd/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_pgd/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)

### `PGD Commit Scopes Configuration`

See examples for PGD Commit Scopes available at: [EDB PGD v5](https://www.enterprisedb.com/docs/pgd/5/durability/commit-scopes/).

The code below is part of the [roles/setup_pgd/defaults/main.yml](./defaults/main.yml), and 
example for configuring two PGD commit scopes is listed below.

The configuration requirements for PGD through the configuration setting variables are:
  1. Only one scope can be configured as default at a time. The variable to configure is: `default_group_cs`
  2. The length of the `member_nodes` for a `camo` commit scope is exactly `two`
  3. No node in `member_nodes` for either commit scope can belong to the other commit scope
  4. All nodes in `member_nodes` must belong to a `parent_group`
  5. The `cs_rule` parameter must be: valid, correctly formatted, and adhere to the correct syntax

COMMIT AT MOST ONCE SCOPE - CAMO
```yaml
pgd_commit_scopes:
  - cs_name: 'camo_scope_1'
    cs_type: 'CAMO'
    parent_group: 'pgd_cluster'
    cs_origin_node_group: 'pgd_two_nodes'
    member_nodes: ['edb-primary1', 'edb-primary2']
    default_group_cs: true
    cs_rule: "ALL ( pgd_two_nodes ) ON visible CAMO DEGRADE ON (timeout=500s) TO ASYNC"
```

GROUP COMMIT SCOPE
```yaml
pgd_commit_scopes:
  - cs_name: 'groupcommit_scope_1'
    cs_type: 'GROUP_COMMIT'
    parent_group: 'pgd_cluster'
    cs_origin_node_group: 'pgd_remaining_nodes'
    member_nodes: ['edb-primary3']
    default_group_cs: true
    cs_rule: "ALL ( pgd_remaining_nodes ) GROUP COMMIT"
```

Host Variables
--------------

### `node_kind`

The role of node to initialize within PGD. Options are `data`, `subscribe-only`, `witness` and `standby`.

### `use_physical_backup`

Set to `true` if you want to initialize non-lead-primary nodes from physical backup.

### `clustername`

Name of cluster node belongs to.

### `lead_primary`

Set to `true` if node is lead primary.

### `location`

HA location of node. 

Dependencies
------------

This role does not have any dependencies, but package repositories should have been 
configured beforehand with the `setup_repo` role. At least one lead primary must exist
and a database cluster must be initialized on that node. 
=======

### `PGD Commit Scopes Configuration`

The code below is part of the [roles/setup_pgd/defaults/main.yml](./defaults/main.yml), and 
example for configuring two PGD commit scopes is listed below.

The configuration requirements for PGD through the configuration setting variables are:
  1. Only one scope can be configured as default at a time. The variable to configure is: `default_group_cs`
  2. The length of the `member_nodes` for a `camo` commit scope is exactly `two`
  3. No node in `member_nodes` for either commit scope can belong to the other commit scope
  4. All nodes in `member_nodes` must belong to a `parent_group`
  5. The `cs_rule` parameter must be: valid, correctly formatted, and adhere to the correct syntax

```yaml
pgd_commit_scopes:
  - cs_name: 'camo_scope_1'
    cs_type: 'CAMO' # either camo or group_commit
    parent_group: 'pgd_cluster' # this group is present in cluster
    cs_origin_node_group: 'pgd_two_nodes' # this group may or may not be present
    member_nodes: ['edb-primary1', 'edb-primary2']
    default_group_cs: true # don't make mandatory, default('false') if not present in array
    cs_rule: "ALL ( pgd_two_nodes ) ON visible CAMO DEGRADE ON (timeout=500s) TO ASYNC"
  - cs_name: 'groupcommit_scope_1'
    cs_type: 'GROUP_COMMIT'
    parent_group: 'pgd_cluster'
    cs_origin_node_group: 'pgd_remaining_nodes'
    member_nodes: ['edb-primary3']
    default_group_cs: false
    cs_rule: "ALL ( pgd_remaining_nodes ) GROUP COMMIT"
```


Example Playbook
----------------

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        edb-primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          location: PGD_DC1
          pgd:
            node_kind: data
            lead_primary: true
            clustername: pgdcluster
        edb-primary2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          location: PGD_DC1
          pgd:
            node_kind: data
            lead_primary: false
            clustername: pgdcluster
            use_physical_backup: true
            upstream_node_private_ip: xxx.xxx.xxx.xxx
        edb-primary3:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          location: PGD_DC1
          pgd:
            node_kind: data
            lead_primary: false
            clustername: pgdcluster
            use_physical_backup: false
```

### How to include the `setup_pgd` role in your Playbook

Below is an example of how to include the `setup_pgd` role:

```yaml
- hosts: all
  name: Postgres deployment playbook
  become: true
  gather_facts: true
  any_errors_fatal: true
  max_fail_percentage: 0

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      ansible.builtin.set_fact:
        pg_version: 15            # Change the version of Postgres you want to install
        pg_type: "EPAS"           # Change the pg_type to EPAS if EDB Advanced Server is needed
        repo_token: "XXXXXXXXX"   # EDB repo 2.0 token
        edb_enable_tde: false     # Enable TDE
        edb_key_unwrap_cmd: ""    # EDB Unwrap commad to decrypt EDB master key. Use can use KMS command to get the real key
        edb_key_wrap_cmd: ""      # EDB Key wrap command to encrypt EDB master key. User can also use KMS commands to get the key
        edb_master_key: ""        # EDB master key for TDE encryption
        edb_secure_master_key: "" # EDB key or passphrase to encrypt EDB master key
        install_pgd: true         # Install PGD flag for installing PGD
        pgd_version: 5            # Postgres Distributed version
        enable_pgdg_repo: true    # flag/variable for enabling PGD repo

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: install_dbserver
      when: "'install_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: init_dbserver
      when: "'init_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: setup_pgd
      when: "'setup_pgd' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_pgd/defaults/main.yml](./defaults/main.yml)
  * [roles/setup_pgd/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/setup_pgd/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)

License
-------

BSD

Author Information
------------------

Author:

  * Vibhor Kumar
  * Hannah Stoik
  * Doug Ortiz
  * EDB Postgres
  * edb-devops@enterprisedb.com www.enterprisedb.com
