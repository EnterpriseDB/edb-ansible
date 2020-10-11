init_dbserver
=========

This Ansible Galaxy Role Initializes Postgres or EnterpriseDB Postgresql Advanced Server versions: 10, 11 and 12 on Instances previously configured. 

**Not all Distribution or versions are supported on all the operating systems available.**
**For more details refer to the: 'Database Engines Supported' section**

**Note:**
The role does not configure Postgres nor EnterpriseDB Postgres Advanced Server for replication it only installs Postgres or EnterpriseDB Postgres Advanced Server across multiple nodes: Main and Standby.
Should there be a need to configure a Postgres or EnterpriseDB Postgres Advanced Server Cluster for replication you can utilize the **setup_replication** role.

**The ansible playbook must be executed under an account that has full privileges.**

Requirements
------------

The only dependencies required for this ansible galaxy role are:

1. Ansible
2. postgresql_set Ansible Module - Utilized when creating aditional users during a Postgres Install
3. setup_repo and install_dbserver - These roles must have been previously executed on the cluster

Role Variables
--------------

When executing the role via ansible there are two required variables:

* os
  Operating Systems supported are: CentOS7 and RHEL7
* pg_version
  Postgres Versions supported are: 10, 11 and 12
* pg_type
  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the 'pre_tasks' definition of the section: 'How to include the 'init_dbserver' role in your Playbook'



The rest of the variables can be configured and are available in the:
* [roles/init_dbserver/vars/edb-pg.yml](./vars/edb-pg.yml) 
* [roles/init_dbserver/vars/edb-epas.yml](./vars/edb-epas.yml) 



Dependencies
------------

The init_dbserver role does depend on the following roles:

* install_dbserver
* setup_repo

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



How to include the 'init_dbserver' role in your Playbook
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
            efm_version: 4.0
            pg_data: "/data/pgdata"

      roles:
        - init_dbserver

**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/init_dbserver/vars/EPAS.yml](./vars/EPAS.yml) 
- [roles/init_dbserver/vars/PG.yml](./vars/PG.yml) 

Database Engines Supported
----------------

Community Postgresql
----------------

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

Enterprise DB Postgresql Advanced Server
----------------

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported




Playbook Execution Examples
----------------

CentOS 7: Community Postgresql with command line parameters
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=10 pg_typeE=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=11 pg_type=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=12 pg_type=PG"

CentOS 7: EDB Advanced Server with command line parameters
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=10 pg_type=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=11 pg_type=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="os=CentOS7 pg_version=12 pg_type=EPAS"


RHEL 7: Community Postgresql with command line parameters
----------------


    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=10 pg_type=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=11 pg_type=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=12 pg_type=PG"


RHEL 7: Enterprise Postgresql with command line parameters
----------------


    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=10 pg_type=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=11 pg_type=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="os=RHEL7 pg_version=12 pg_type=EPAS"


CentOS 7: Community Postgresql without command line parameters
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem>


CentOS 7: Enterprise Postgresql without command line parameters
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem>


RHEL 7: Community Postgresql without command line parameters
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>


RHEL 7: Enterprise Postgresql without command line parameters
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>


 


License
-------

BSD

Author Information
------------------
Author: 
* Doug Ortiz
* Vibhor Kumar (Reviewer)
* EDB Postgres 
* DevOps 
* doug.ortiz@enterprisedb.com www.enterprisedb.com
