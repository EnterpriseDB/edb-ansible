install_dbserver
=========

This Ansible Galaxy Role Installs Postgres or EnterpriseDB Postgresql Advanced Server versions: 10, 11 and 12 on Instances previously configured. 

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
3. edb-devops.postgres -> setup_repo role for setting the repository on the systems

Role Variables
--------------

When executing the role via ansible these are the required variables:

* OS
  Operating Systems supported are: CentOS7 and RHEL7
* PG_VERSION
  Postgres Versions supported are: 10, 11 and 12
* PG_TYPE
  Database Engine supported are: PG and EPAS

These and other variables can be assigned in the 'pre_tasks' definition of the section: 'How to include the 'install_dbserver' role in your Playbook'



The rest of the variables can be configured and are available in the:
* [roles/install_dbserver/defaults/main.yml](./defaults/main.yml) 



Dependencies
------------

The install_dbserver role does not have any dependencies on any other roles.

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



How to include the 'install_dbserver' role in your Playbook
----------------

Below is an example of how to include the install_dbserver role:



    - hosts: localhost
      name: Install Postgres on Instances
      #connection: local
      become: true
      gather_facts: no
 
      collections:
        - edb_devops.postgres

      vars_files:
        - hosts.yml

      pre_tasks:
        # Define and assign any variables that
        # have been previously defined in role
        # or that are new
        - set_fact:
            OS: "CentOS7"
            PG_TYPE: "PG"
            PG_VERSION: "12"
          with_dict: "{{ servers }}"

      tasks:
        - name: Iterate through role with items from hosts file
          include_role:
            name: install_dbserver
          with_dict: "{{ servers }}"


**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/install_dbserver/defaults/main.yml](./defaults/main.yml)

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


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=10 PG_TYPE=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=11 PG_TYPE=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=12 PG_TYPE=PG"

CentOS 7: Enterprise Postgresql with command line parameters
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=10 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=11 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=12 PG_TYPE=EPAS"


RHEL 7: Community Postgresql with command line parameters
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=10 PG_TYPE=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=11 PG_TYPE=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=12 PG_TYPE=PG"


RHEL 7: Enterprise Postgresql with command line parameters
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=10 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=11 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=12 PG_TYPE=EPAS"


CentOS 7: Community Postgresql without command line parameters
----------------

    ansible-playbook playbook.yml -u centos -- private-key <key.pem>


RHEL 7: Community Postgresql without command line parameters
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
