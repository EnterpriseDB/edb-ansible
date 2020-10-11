
setup_replication
=========
This Ansible Galaxy Role configures Replication on Postgres or EnterpriseDB Postgres Advanced Server versions: 10, 11 and 12 on Instances previously configured.


Requirements
------------

The only dependencies required for this ansible galaxy role are:

1. Ansible
2. postgresql_set Ansible Module - Utilized when creating aditional users during a Postgres Install. Only on primary nodes.
3. setup_repo - for repository installation
4. install_dbserver - for installation of PostgreSQL/EPAS binaries.

Role Variables
--------------

When executing the role via ansible there are three required variables:

* os
  Operating Systems supported are: CentOS7 and RHEL7
* pg_version
  Postgres Versions supported are: 10, 11 and 12
* pg_type
  The type of postgres : EPAS or PG

The rest of the variables can be configured and are available in the:
* [roles/setup_replication/defaults/main.yml](./defaults/main.yml)

Dependencies
------------

The setup_replication role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:


    servers:
       main:
         node_type: primary
         public_ip: xx.xx.xx.xx.             #- Public IP Address for Main Node
         private_ip: xx.xx.xx.xx.            #- Private IP Address for Main Node
       standby1: 
         node_type: standby
         private_ip: xx.xx.xx.xx             #- Private IP Address for Standby1 Node 
         public_ip: xx.xx.xx.xx              #- Public IP Address for Standby1	
         replication_type: asynchronous      #- replication type
       standby2:
         node_type: standby
         private_ip: xx.xx.xx.xx             #- Private IP Address for Standby2 Node
         public_ip: 3.84.161.181             #- Public IP Address for Standby2
         replication_type: asynchronous      #- replication type
   



How to include the 'setup_replication' role in your Playbook
----------------

Below is an example of how to include the setup_replication role:



    - hosts: localhost
      name: Install EDB replication on Instances
      connection: local
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
            pg_data: "/data/pgdata"

      roles:
        - setup_replication


**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/setup_replication/vars/edb-epas.yml](./vars/edb-epas.yml) 
- [roles/setup_replication/vars/edb-pg.yml](./vars/edb-pg.yml) 

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

CentOS 7 with command line parameters:
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 pg_version=10 pg_type=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 pg_version=11 pg_type=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 pg_version=12 pg_type=EPAS"
  

RHEL 7 with command line parameters:
----------------


    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 pg_version=10 pg_type=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 pg_version=11 pg_type=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 pg_version=12 pg_type=EPAS"


CentOS 7 without command line parameters:
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem>
  

RHEL 7 without command line parameters:
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>



License
-------

BSD
