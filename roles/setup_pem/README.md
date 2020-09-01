setup_pem
=========

This Ansible Galaxy Role Installs and configure PEM on Instances previously configured.

**Note:**
The role only installs EPAS: 10, 11 or 12 along with EFM: 3.7, 3.8 or 3.9 across multiple nodes.

**Not all Distribution or versions are supported on all the operating systems available.**
**For more details refer to the: 'Database Engines Supported' section**

**Note:**
The role does not configure EDB Postgres Advanced Server or PostgreSQL for replication it only installs Postgres Enterprise Manager (PEM) agents across multiple nodes and configure database nodes for PEM monitornig and configures any node to be a PEM server.
If you want to configure EDB Advanced Server Cluster of PostgreSQL, then please use the 'setup_replication' module:
1. setup_repo : For installing the EPAS/PG repository
2. install_dbserver: For installing the EPAS/PG binaries
3. init_dbserver: For initializing the EPAS/PG data directory and configuring a primary/master node.
4. setup_replication: For creating the standby.
5. setup_efm: For managing and maintaing the HA of the Postgres cluster

**The ansible playbook must be executed under an account that has full privileges.**

Requirements
------------

The only dependencies required for this ansible galaxy role are:

1. Ansible >= 2.9

Role Variables
--------------

When executing the role via ansible the variables listed below are required:

* OS
  Operating Systems supported are: CentOS7 and RHEL7
* PG_TYPE
  Install Type supported are: EPAS
* PG_VERSION
  EPAS Versions supported are: 10, 11 and 12
* EFM_VERSION
  EFM Versions supported are: 3.7, 3.8 and 3.9



The rest of the variables can be configured and are available in the:
* [roles/setup_pem/defaults/main.yml](./defaults/main.yml) 

Dependencies
------------

The setup_pem role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:    

     servers:
        pemserver:
          node_type: pemserver
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        main:
          node_type: primary
          pem_agent: true
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        standby1:
          node_type: standby1
          pem_agent: true
          replication_type: asynchronous
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        standby2:
          node_type: standby2
          pem_agent: true
          replication_type: asynchronous
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx
        witness:
          node_type: witness
          pem_agent: true
          private_ip: xxx.xxx.xxx.xxx
          public_ip: xxx.xxx.xxx.xxx



How to include the 'setup_pem' role in your Playbook
----------------

Below is an example of how to include the setup_pem role:



    - hosts: localhost
      name: Setup PEM on Instances
      #connection: local
      become: true
      gather_facts: no

      collections:
        - edb_devops.edb_postgres
    
      vars_files:
        - hosts.yml
  
      #initializing some variables
      vars:
        PEM_SERVER_PRIVATE_IP: ""
        PRIMARY_PRIVATE_IP: ""
        PRIMARY_PUBLIC_IP: ""
        STANDBY_NAMES: []
        ALL_NODE_IPS: []
        EFM_NODES_PRIVATE_IP: []
        EFM_NODES_PUBLIC_IP: []

      pre_tasks:
        # Define or re-define any variables previously assigned
        - name: Initialize the user defined variables
          set_fact:
            OS: "OS"
            PG_TYPE: "PG_TYPE"
            PG_VERSION: "PG_VERSION"
            EFM_VERSION: "EFM_VERSION"
            PG_DATA: "/data/pgdata"
            PG_EFM_USER: "efm"
            PG_EFM_USER_PASSWORD: "efm"
            ALL_NODE_IPS: "{{ ALL_NODE_IPS + [item.value.private_ip] }}"
            PEM_SERVER_PRIVATE_IP: "{{ PEM_SERVER_PRIVATE_IP + item.value.private_ip if(item.value.node_type == 'pemserver') else PEM_SERVER_PRIVATE_IP }}"
            PRIMARY_PRIVATE_IP: "{{ PRIMARY_PRIVATE_IP + item.value.private_ip if(item.value.node_type == 'primary') else PRIMARY_PRIVATE_IP }}"
            PRIMARY_PUBLIC_IP: "{{ PRIMARY_PUBLIC_IP  + item.value.public_ip if(item.value.node_type == 'primary') else PRIMARY_PUBLIC_IP }}"
          with_dict: "{{ servers }}"
         
        - name: Gather primary and standby nodes for EFM
          set_fact:
            EFM_NODES_PRIVATE_IP: "{{ EFM_NODES_PRIVATE_IP + [item.value.private_ip] }}"
            EFM_NODES_PUBLIC_IP: "{{ EFM_NODES_PUBLIC_IP + [item.value.public_ip] }}"
          when: item.value.node_type in ['primary', 'standby']
          with_dict: "{{ servers }}"
  
        - name: Gather the standby names
          set_fact:
            STANDBY_NAMES: "{{ STANDBY_NAMES + [item.key] }}"
          when: item.value.node_type == 'standby'
          with_dict: "{{ servers }}"
          
      tasks:
        - name: Iterate through role with items from hosts file
          include_role:
            name: setup_pem
          with_dict: "{{ servers }}"


**Two example playbooks for setting up PEM with CentOS7 and RHEL7 are available in the [playbook-examples](/playbook-examples) directory.**

**Defining and adding variables can be done in the set_fact of the pre-tasks.**

All the variables are available at:
- [roles/setup_pem/vars/edb-epas.yml](./vars/edb-epas.yml) 
- [roles/setup_pem/vars/edb-pg.yml](./vars/edb-pg.yml) 


Database Engines Supported
----------------

Postgres Enterprise Manager:
----------------

| Postgres | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



| Enterprise Postgres Advanced Server | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



Postgres Enterprise Manager:
----------------

| Postgres | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



| Enterprise Postgres Advanced Server | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



Postgres Enterprise Manager:
----------------

| Postgres | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



| Enterprise Postgres Advanced Server | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|

- :white_check_mark: - Tested and supported
- :x: - Not supported



Playbook Execution Examples
----------------

Postgresql - CentOS 7:
----------------

    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG PG_VERSION=10 EFM_VERSION=3.7"
    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG PG_VERSION=11 EFM_VERSION=3.9"
    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=PG PG_VERSION=12 EFM_VERSION=3.9"


Postgresql - RHEL 7:
----------------

    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG PG_VERSION=10 EFM_VERSION=3.7"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG PG_VERSION=11 EFM_VERSION=3.8"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=PG PG_VERSION=12 EFM_VERSION=3.9"



EnterpriseDB Postgresql Advanced Server - CentOS 7:
----------------

    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS PG_VERSION=10 EFM_VERSION=3.7"
    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS PG_VERSION=11 EFM_VERSION=3.9"
    ansible-playbook playbook.yml -u centos --private-key <key.pem> --extra-vars="OS=CentOS7 PG_TYPE=EPAS PG_VERSION=12 EFM_VERSION=3.9"


EnterpriseDB Postgresql Advanced Server - RHEL 7:
----------------

    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS PG_VERSION=10 EFM_VERSION=3.7"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS PG_VERSION=11 EFM_VERSION=3.8"
    ansible-playbook playbook.yml -u ec2-user --private-key <key.pem> --extra-vars="OS=RHEL7 PG_TYPE=EPAS PG_VERSION=12 EFM_VERSION=3.9"



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
