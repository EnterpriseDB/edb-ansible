postgres
=========

This Ansible Galaxy Collection sets up and configures the repositories from which packages will be retrieved for any Postgres or EnterpriseDB Postgresql Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems available.**

**The ansible playbook must be executed under an account that has full privileges.**


edb-ansible is a repository used for hosting an Ansible Collection that currently supports the following ansible roles:

## setup_repo: 
A role for setting up the EDB and PG Community and EPEL repositories. For installation of these repositories, role needs outbound connections to internet, mainly connection to the following sites:
   1. yum.enterprisedb.com
   2. download.postgresql.org
   3. dl.fedoraproject.org
This role requires following compulsory parameters:
* `PG_TYPE`: "EPAS" or "PG"
* `EDB_YUM_USERNAME`: EDB repository's username
* `EDB_YUM_PASSWORD`: EDB yum repository's password.

For access to EDB repository, you can use following link: [EDB yum access ](https://www.enterprisedb.com/user/register?destination=/repository-access-request%3Fdestination%3Dnode/1255704%26resource%3D1255704%26ma_formid%3D2098)


* install_dbserver: A role for installing EPAS/PG database server packages. This role installs the PG/EEPAS packages, depending on the `PG_TYPE` and `PG_VERSION` variables' setting in the playbook.yml.

* init_dbserver: A role for initializing the PG/EDB cluster(data) directory. This role allows users to pass following variables:
1. `PG_TYPE`: EPAS/PG
2. `PG_VERSION`: EPAS/PG Version. Default is 12. 
3. `PG_DATA`: EPAS/PG data directory. Default is /var/lib/edb/as{PG_VERSION}/data
4. `PG_WAL`: EPAS/PG wal location. Default is /var/lib/edb/as{PG_VERSION}/data/pg_wal
5. `PG_SSL`: For configuration of data directory with SSL
6. `PG_SSL_DIR`: Location of ssl files. Due to security reasons, default location is /etc/edb/certs.
**Note**: In case, users want to use their certificates, then it is recommended to set `PG_SSL_GENERATE` to false and place their certificate in /etc/edb/certs directory or directory.
7. `PG_SSL_GENERATE`: Default is True. Allow role to generate SSL certificates with the initialization of the database cluster.
9. `PG_ENCODING`: Database encoding. Default "UTF-8"


For more informtion on variables, please refere to the following variables file:
1. EPAS variables [init_dbserver/vars/edb-epas.yml](./init_dbserver/vars/edb-epas.yml) 
2. And, PG variables [init_dbserver/vars/edb-pg.yml](./init_dbserver/edb-pg.yml)

In case user wants to manage normal database users, then they can use following varaible and syntax in the playbook:
`PG_USERS
    - name: app1_user
      pass: password
    - name: app2_user
      pass: password`
      
For user defined databases:
`PG_DATABASES:
    - name: app_db1
      owner: app_user1`
      
In case a user wants to pass set specific PG/EPAS parameters, following variables can be set in playbook:
`PG_POSTGRES_CONF_PARAMS:
    - { name: "maintenance_work_mem", value: "1GB" }
    - { name: "work_mem", value: "1024MB" }`

For setting specific pg_hba.conf rule, following varaible can be used:
`PG_ALLOW_IP_ADDRESSES:
    - { user: "user1,user2", ip_address: "172.0.0.1/16", databases: "db1,db2" }
    - { user: "user3,user4", ip_address: "172.128.0.1/16", databases: "db3,db4" }`
    
* setup_replication: A role for setting up the replication (synchronous/asynchronous)
* setup_efm: A role for setting up Failover Manager for Postgres/EPAS HA cluster.

In the playbook, user can choose the specific roles based on their requirement.

Prerequiste
----------------
For correctly installed and configuration of the cluster following are requirements:
1. Following are ports which should be opened for communication between the servers
    Postgres/EPAS port:  5432/5444
    EDB Failover Manager: 7800-7810
  **Note**: If you have firewall enabled on the server, then please allow the access through above ports. 
2. Ansible (on the machine on which playbook will be executed).
3. Operating system privileged user (user with sudo privilege) on all the servers/virtual machines.
**Note**: In our examples, we have used centos user for CentOS OS and ec2_user for RHEL OS as a privileged user.


Items to be aware 
----------------

* Security in your environment

* Services enabled on your instances, such as: Firewalld



Installation Steps
----------------

The 'postgres' Ansible collection can be installed by two different steps:

* [Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* Installing the 'postgres' Ansible Collection
* Downloading the 'postgres' repository source code from the repository in GitHub
* Cloning the 'postgres' repository source code from the repository in GitHub


Installing the 'postgres' Ansible Collection
----------------
Installing the 'postgres' Ansible Collection is done by following the steps below:

      ansible-galaxy collection install edb-devops.postgres --force

**This step does automatically make the 'postgres' collection available to your playbooks.**

**A message indicating where the collection is installed will be displayed by ansible-galaxy. The collection code should be automatically made readily available for you.**

**By default the location of your installed collection is: ~/.ansible/collections/ansible_collections**



Downloading the 'postgres' repository source code from the repository in GitHub
----------------
Downloading the code from the repository can be accomplished by following the steps below:

      * Navigate to the repository address: https://github.com/EnterpriseDB/edb-ansible
      * Click on the green *Code* Button located next to the *About* section
      * Click on the *Download Zip* Link menu option

**After the code has been downloaded, the code will be available as a zip file which requires being unzipped to your desired target destination.**

**This step does not automatically make the 'postgres' collection available to your playbooks.**


Cloning the 'postgres' repository source code from the repository GitHub
----------------
Downloading the code from the repository can be accomplished by following the steps below:

      git clone git@github.com:EnterpriseDB/edb-ansible.git

**After the code has been downloaded, the code will be available in your current directory within a directory named: 'edb-ansible'.**

You can access the root folder of the repository by entering the command below:

      cd edb-ansible

**This step does not automatically make the 'postgres' collection available to your playbooks.**

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
