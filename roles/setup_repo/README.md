setup_repo
=========

This Ansible Galaxy Role sets up and configures the repositories from which packages will be retrieved for any Postgres or EnterpriseDB Postgresql Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems available.**
**For more details refer to the: Database Engines Supported section**

**Note:**
The role does not configure Postgres nor EnterpriseDB Postgres Advanced Server for replication it only installs Postgres or EnterpriseDB Postgres Advanced Server across multiple nodes.
Should there be a need to install and/or configure a Postgres or EnterpriseDB Postgres Advanced Server Cluster you can utilize the **install_dbserver** role.

**The ansible playbook must be executed under an account that has full privileges.**

Requirements
------------

The only dependencies required for this ansible galaxy role are:

1. Ansible

Role Variables
--------------

When executing the role via ansible these are the required variables:

* OS
  Operating Systems supported are: CentOS7 and RHEL7
* PG_TYPE
  Database Engine supported are: PG and EPAS
* EDB_YUM_USERNAME
  If you have PG_TYPE = EPAS, then you need to include EDB_YUM_USERNAME
* EDB_YUM_PASSWORD
  If you have PG_TYPE = EPAS, then you need to include EDB_YUM_PASSWORD



The rest of the variables can be configured and are available in the:
* [roles/setup_repo/defaults/main.yml](./defaults/main.yml) 



Dependencies
------------

The setup_repo role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:



      hosts:
        primary:
          node_type: primary
          public_ip: xxx.xxx.xxx.xxx
        standby11:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
        standby12:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx



How to include the 'setup_repo' role in your Playbook
----------------

Below is an example of how to include the setup_repo role:



    - hosts: localhost
      name: Setup and Configure Repos for package retrievals
      connection: local
      become: true
      gather_facts: no

      vars_files:
        - hosts.yml

      pre_tasks:
        # Define or re-define any variables previously assigned
        - set_fact:
            OS: OS
            PG_TYPE: PG_TYPE
            EDB_YUM_USERNAME: ""
            EDB_YUM_PASSWORD: ""
          with_dict: "{{ hosts }}"

      tasks:
        - name: Iterate through role with items from hosts file
          include_role:
            name: setup_repo
          with_dict: "{{ hosts }}"


**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/setup_repo/defaults/main.yml](./defaults/main.yml) 


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

CentOS 7: Community Postgresql
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG"

CentOS 7: Enterprise Postgresql
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS"


RHEL 7: Community Postgresql
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG"


RHEL 7: Enterprise Postgresql
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS"

 
Debian: Community Postgresql
----------------

     Not Supported.


Debian: Enterprise Postgresql
----------------
     Not Supported.


Ubuntu: Community Postgresql
----------------

     Not Supported.


Ubuntu: Enterprise Postgresql
----------------

     Not Supported.



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
