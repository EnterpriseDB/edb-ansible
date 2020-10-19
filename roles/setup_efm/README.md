setup_efm
=========

This Ansible Galaxy Role Installs EFM versions: 3.10 and 4.0 on instances previously configured.

**Note:**
The role only installs EPAS: 10, 11, 12 or 4.0 along with EFM: 3.9 or 4.0 across multiple nodes.

**Not all Distribution or versions are supported on all the operating systems available.**
**For more details refer to the: 'Database Engines Supported' section**

**Note:**
The role does not configure EDB Postgres Advanced Server or PostgreSQL for replication it only installs EDB Postgres Failover Manager (EFM) across multiple nodes and configure database nodes for EFM monitornig and HA management.
If you want to configure EDB Advanced Server Cluster of PostgreSQL, then please use the 'setup_replication' module:
1. community.general 
2. setup_repo : For installing the EPAS/PG repository
3. install_dbserver: For installing the EPAS/PG binaries
4. init_dbserver: For initializing the EPAS/PG data directory and configuring a primary/master node.
5. setup_replication: For creating the standby.

**The ansible playbook must be executed under an account that has full privileges.**

Requirements
------------

The only dependencies required for this ansible galaxy role are:

1. Ansible >= 2.9

Role Variables
--------------

When executing the role via ansible the variables listed below are required:

When executing the role via ansible these are the required variables:

* <strong> <em> os </em> </strong>

  Operating Systems supported are: CentOS7, RHEL7, CentOS8 and RHEL8

* <strong> <em> pg_version </em> </strong>

  Postgres Versions supported are: 10, 11, and 12

* <strong> <em> pg_type </em> </strong>

  Database Engine supported are: PG and EPAS


The rest of the variables can be configured and are available in the:
* [roles/setup_efm/defaults/main.yml](./defaults/main.yml) 
* [roles/setup_efm/vars/EPAS.yml](./vars/EPAS.yml) 
* [roles/setup_efm/vars/PG.yml](./vars/PG.yml) 

Dependencies
------------

The setup_efm role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:    

     servers:
        main:
          node_type: primary
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        standby1:
          node_type: standby1
          replication_type: asynchronous
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        standby2:
          node_type: standby2
          replication_type: asynchronous
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        witness:
          node_type: witness
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx



How to include the 'setup_efm' role in your Playbook
----------------

Below is an example of how to include the setup_efm role:



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
            os: "os"
            pg_type: "pg_type"
            pg_version: "pg_version"
            efm_version: "efm_version"
            efm_parameters:
                  - name: script.notification
                    value: "/usr/edb/efm-4.0/bin/notification.sh"
                  
      roles:
        - setup_efm


**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/setup_efm/vars/EPAS.yml](./vars/EPAS.yml) 
- [roles/setup_efm/vars/PG.yml](./vars/PG.yml) 


Database Engines Supported
----------------

EnterpriseDB Failover Manager 3.10/4.0:
----------------

| Postgres | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 8 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

Enterprise DB Postgresql Advanced Server
----------------

| Enterprise Postgres Advanced Server | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| CentOS 8 | :x:| :x:| :white_check_mark:|
| Red Hat Linux 8 | :x:| :x:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported




Playbook Execution Examples
----------------

CentOS/RHEL: Community Postgresql with command line parameters
----------------


    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="os=CentOS7 pg_version=12 pg_type=PG efm_version=4.0"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="os=RHEL7 pg_version=12 pg_type=EPAS efm_version=4.0"
    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="os=CentOS8 pg_version=12 pg_type=PG efm_version=4.0"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="os=RHEL8 pg_version=12 pg_type=EPAS efm_version=4.0"


CentOS/RHEL 7/8: Community Postgresql without command line parameters
----------------

    ansible-playbook playbook.yml -u centos --private-key <key.pem>
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem>




License
-------

BSD

Author Information
------------------
Author: 
* Doug Ortiz
* Vibhor Kumar (Co-Author)
* EDB Postgres 
* DevOps 
* doug.ortiz@enterprisedb.com www.enterprisedb.com
