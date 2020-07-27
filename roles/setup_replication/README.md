
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

When executing the role via ansible there are two required variables:

* OS
  Operating Systems supported are: CentOS7 and RHEL7
* PG_VERSION
  Postgres Versions supported are: 10, 11 and 12
* PG_TYPE
  The type of postgres : EPAS or PG

The rest of the variables can be configured and are available in the:
* [roles/setup_replication/defaults/main.yml](./defaults/main.yml)

Dependencies
------------

The setup_replication role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:


     hosts:
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

      vars_files:
        - hosts.yml
  
      #initializing some variables
      vars:
        PRIMARY_PRIVATE_IP: ""
        PRIMARY_PUBLIC_IP: ""
        STANDBY_NAMES: []
        ALL_NODE_IPS: []

      pre_tasks:
        # Define or re-define any variables previously assigned
        - set_fact:
            OS: "OS"
            PG_TYPE: "PG_TYPE"
            PG_VERSION: "PG_VERSION"
            EFM_VERSION: "EFM_VERSION"
            PG_DATA: "/data/pgdata"

            # Variables for internal processing
            ALL_NODE_IPS: "{{ ALL_NODE_IPS + [item.value.private_ip] }}"
            PRIMARY_PRIVATE_IP: "{{ PRIMARY + item.value.private_ip if(item.value.node_type == 'main') else PRIMARY }}"
            PRIMARY_PUBLIC_IP: "{{ PRIMARY_PUBLIC_IP  + item.value.public_ip if(item.value.node_type == 'main') else PRIMARY_PUBLIC_IP }}"
          with_dict: "{{ hosts }}"       
        - set_fact:
            STANDBY_NAMES: "{{ STANDBY_NAMES + [item.key] }}"
          when: item.value.node_type == 'standby'
          with_dict: "{{ hosts }}"
      tasks:
        - name: Iterate through role with items from hosts file
          include_role:
            name: setup_replication
          with_dict: "{{ hosts }}"


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


    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=10 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=11 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u centos -- private-key <key.pem> --extra-vars="OS=CentOS7 PG_VERSION=12 PG_TYPE=EPAS"
  

RHEL 7 with command line parameters:
----------------


    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=10 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=11 PG_TYPE=EPAS"
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem> --extra-vars="OS=RHEL7 PG_VERSION=12 PG_TYPE=EPAS"


CentOS 7 without command line parameters:
----------------


    ansible-playbook playbook.yml -u centos -- private-key <key.pem>
    ansible-playbook playbook.yml -u centos -- private-key <key.pem>
    ansible-playbook playbook.yml -u centos -- private-key <key.pem>
  

RHEL 7 without command line parameters:
----------------

    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>
    ansible-playbook playbook.yml -u ec2-user -- private-key <key.pem>



License
-------

BSD
