postgres
=========

This Ansible Galaxy Collection sets up and configures the repositories from which packages will be retrieved for any Postgres or EnterpriseDB Postgresql Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems available.**

**The ansible playbook must be executed under an account that has full privileges.**


Description
------------

edb-ansible is a repository used for hosting an Ansible Collection that currently supports the following ansible roles:

* setup_repo
* install_dbserver
* init_dbserver
* setup_replication
* setup_efm


Ports to be aware that require to be available
----------------

Postgres:

      5432

EDB Postgres Advanced Server:

      5444
 
EDB Failover Manager:

      7800 through 7810



Items to be aware 
----------------

* Security in your environment

* Services enabled on your instances, such as: Firewalld



Installation Steps
----------------

The 'postgres' Ansible collection can be installed by two different steps:

* Ansible galaxy
* Utilizing git to download the source code of the from the repository


Installing the 'postgres' Ansible Collection
----------------
Installing the 'postgres' Ansible Collection is done by following the steps below:

      ansible-galaxy collection install edb-devops.postgres --force

**A message indicating where the collection is installed will be displayed by ansible-galaxy. The collection code should be automatically made readily available for you.**



Downloading the 'postgres' repository source code from the repository in GitHub
----------------
Downloading the code from the repository can be accomplished by following the steps below:

      git clone git@github.com:EnterpriseDB/edb-ansible.git

**After the code has been downloaded, the code will be available in your current directory within a directory named: 'edb-ansible'.**

You can access the root folder of the repository by entering the command below:

      cd edb-ansible


Hosts file content
----------------

Content of the hosts.yml file:

      hosts:
        main1:
          node_type: primary
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
        standby11:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
        standby12:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous



How to include the roles in your Playbook
----------------

Below is an example of how to include the setup_repo role:

    - hosts: localhost
      # Un-comment to specify which python interpreter to utilize
      #vars:
      #  ansible_python_interpreter: /usr/bin/python2
      name: Install, Configure, Initialize and Replication EDB Postgres Advanced Server 12 and EFM 10 on Instances
      #connection: local
      become: true
      gather_facts: no
   
      collections:
        - edb-devops.postgres

      vars_files:
        - hosts.yml

      vars:
        PRIMARY_PRIVATE_IP: ""
        PRIMARY_PUBLIC_IP: ""
        STANDBY_NAMES: []
        ALL_NODE_IPS: []

      # Internal processing purposes only
      pre_tasks:
        # Define or re-define any variables previously assigned
        - name: Initialize the user defined variables
          set_fact:
            # 'CentOS7' or 'RHEL7'
            OS: "CentOS7"
            # 'PG' or 'EPAS'
            PG_TYPE: "EPAS"
            PG_DATA: "/data/pgdata"
            PG_WAL: "/data/pg_wal"
            # Ensure you enter your credentials when utilizing EDB custom repositories
            EDB_YUM_USERNAME: ""
            EDB_YUM_PASSWORD: ""
            STANDBY_QUORUM_TYPE: "ANY" # Quorum type can be ANY or FIRST
            ALL_NODE_IPS: "{{ ALL_NODE_IPS + [item.value.private_ip] }}"
            PRIMARY_PRIVATE_IP: "{{ PRIMARY_PRIVATE_IP + item.value.private_ip if(item.value.node_type == 'primary') else PRIMARY_PRIVATE_IP }}"
            PRIMARY_PUBLIC_IP: "{{ PRIMARY_PUBLIC_IP  + item.value.public_ip if(item.value.node_type == 'primary') else PRIMARY_PUBLIC_IP }}"
          with_dict: "{{ hosts }}"
          
        - name: Gather the standby names
          set_fact:
            STANDBY_NAMES: "{{ STANDBY_NAMES + [item.key] }}"
          when: item.value.node_type == 'standby'
          with_dict: "{{ hosts }}"

      tasks:
        - name: Iterate through role with items from hosts file
          include_role:
            name: setup_repo
          with_dict: "{{ hosts }}"
        - name: Iterate through install role with items from hosts file
          include_role:
            name: install_dbserver
          with_dict: "{{ hosts }}"
        - name: Iterate through initialize role with items from hosts file
          include_role:
            name: init_dbserver
          with_dict: "{{ hosts }}"
        - name: Iterate through replication role with items from hosts file
          include_role:
            name: setup_replication
          with_dict: "{{ hosts }}"
        - name: Iterate through efm install role with items from hosts file
          include_role:
            name: setup_efm
          with_dict: "{{ hosts }}"
 

**Defining and adding variables can be done in the set_fact of the pre-tasks.**

**You can customize the above example to install 'Postgres', 'EPAS', 'EFM' or limit what roles you would like to execute: 'setup_repo', 'install_dbserver', 'init_dbserver', 'setup_replication' or 'setup_efm'.**



Executing the playbook:
----------------

CentOS7

      ansible-playbook -private-key=<yourprivatekey> playbook.yml -u centos

RHEL7

       ansible-playbook -private-key=<yourprivatekey> playbook.yml -u ec2-user




Database Engines Supported
----------------

Community Postgresql
----------------

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: |

Enterprise DB Postgresql Advanced Server
----------------

| Distribution | 10 | 11 | 12 |
| ------------------------- |:--:|:--:|:--:|
| CentOS 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: |
- :white_check_mark: - Tested and supported
- :x: - Not tested and not supported


License
-------

BSD

Author Information
------------------
Author: 
* Doug Ortiz
* Vibhor Kumar (Reviewer)
* Collection Name: postgres 
* DevOps 
* doug.ortiz@enterprisedb.com www.enterprisedb.com
