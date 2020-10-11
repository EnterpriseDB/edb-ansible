edb_postgres
=========

This Ansible Galaxy Collection sets up and configures the repositories from which packages will be retrieved for any Postgres or EnterpriseDB Postgresql Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems available.**

**The ansible playbook must be executed under an account that has full privileges.**


`edb-ansible` is a repository used for hosting an Ansible Collection that currently supports the following ansible roles:

Roles
-----

### process_vars:

A role for processing the hosts.yml file and setting the required variables for other dependent roles.

### setup_repo: 
A role for setting up the EDB and PG Community and EPEL repositories. For installation of these repositories, role needs outbound connections to internet, mainly connection to the following sites:

```
   1. yum.enterprisedb.com
   2. download.postgresql.org
   3. dl.fedoraproject.org
```

This role requires following compulsory parameters:
* `pg_type`: "EPAS" or "PG"
* `yum_username`: EDB repository's username
* `yum_password`: EDB yum repository's password.

For access to EDB repository, you can use following link: [EDB yum access](https://www.enterprisedb.com/user/register?destination=/repository-access-request%3Fdestination%3Dnode/1255704%26resource%3D1255704%26ma_formid%3D2098)


### install_dbserver: 

A role for installing EPAS/PG database server packages. This role installs the EPAS/PG packages, depending on the values of the following variables in the playbook.yml:

1. `pg_type`: EPAS/PG 
2. And `pg_version`: EPAS/PG major version number


### init_dbserver: 

A role for initializing the PG/EPAS cluster(data) directory. 

This role allows users to pass following variables:

1. `pg_type`: EPAS/PG
2. `pg_version`: EPAS/PG Version. *Default is 12.*
3. `pg_data`: EPAS/PG data directory. *Default is /var/lib/edb/as{pg_version}/data*
4. `pg_wal`: EPAS/PG wal location. *Default is /var/lib/edb/as{pg_version}/data/pg_wal*
5. `pg_ssl`: For configuration of data directory with SSL

For more information on variables, please refer to the following variables file:
1. EPAS variables: [init_dbserver/vars/EPAS.yml](./init_dbserver/vars/EPAS.yml) 
2. And, PG variables: [init_dbserver/vars/PG.yml](./init_dbserver/PG.yml)

For more information on the role, please refer roles README
[README.md](./roles/init_dbserver/README.md)
    
### setup_replication:

A role for setting up the replication (synchronous/asynchronous).
Similar to `init_dbserver` role, `setup_replication` has following variables for managing the EPAS/PG.

1. `pg_type`: EPAS/PG
2. `pg_version`: EPAS/PG Version. *Default is 12.*
3. `pg_data`: EPAS/PG data directory. *Default is /var/lib/edb/as{pg_version}/data*
4. `pg_wal`: EPAS/PG wal location. *Default is /var/lib/edb/as{pg_version}/data/pg_wal*
5. `pg_replication_user`: Replication user for replicating data between primary and standby. *Default is repuser*
6. `pg_replication_user_password`: Replication user password. *Default auto generated and stored on localhost under ~/.edb/<pg_replication_user_password>_pass*

### setup_efm:

A role for setting up EDB Failover Manager for Postgres/EPAS HA cluster.

In the playbook, user can choose the specific roles based on their requirement.

### setup_pem

This role helps in setting PEM Server and deployment of PEM Agent on the PG/EPAS servers.


Prerequisites
----------------
For correctly installed and configuration of the cluster following are requirements:

1. Following are ports which should be opened for communication between the servers
    
    * Postgres:                           5432
    * EDB Postgres Advanced Server Port:  5444
    * EDB Failover Manager:               7800-7810
  
  **Note**: If you have firewall enabled on the server, then please allow the access through above ports. 

2. Ansible (on the machine on which playbook will be executed).
3. Operating system privileged user (user with sudo privilege) on all the servers/virtual machines.

**Note**: In our examples, we have used `centos` user for Centos os and `ec2_user` for RHEL os as a privileged user.

Installation Steps
----------------

The `edb_postgres` Ansible collection can be installed by two different steps:

* [Installing Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
* Installing the `edb_postgres` Ansible Collection
* Downloading the `edb_postgres` repository source code from the repository in GitHub
* Cloning the `edb_postgres` repository source code from the repository in GitHub


### Installing the `edb_postgres` Ansible Collection

Installing the `edb_postgres` Ansible Collection is done by following the steps below:

      ansible-galaxy collection install edb_devops.edb_postgres --force

**This step does automatically make the `edb_postgres` collection available to your playbooks.**

**A message indicating where the collection is installed will be displayed by ansible-galaxy. The collection code should be automatically made readily available for you.**

**By default the location of your installed collection is: ~/.ansible/collections/ansible_collections**



### Downloading the `edb_postgres` repository source code from the repository in GitHub

Downloading the code from the repository can be accomplished by following the steps below:

      * Navigate to the repository address: `https://github.com/EnterpriseDB/edb-ansible`
      * Click on the green *Code* Button located next to the *About* section
      * Click on the *Download Zip* Link menu option

**After the code has been downloaded, the code will be available as a zip file which requires being unzipped to your desired target destination.**

**This step does not automatically make the `postgres` collection available to your playbooks.**


### Cloning the `edb_postgres` repository source code from the repository GitHub

Downloading the code from the repository can be accomplished by following the steps below:

      git clone git@github.com:EnterpriseDB/edb-ansible.git

**After the code has been downloaded, the code will be available in your current directory within a directory named: 'edb-ansible'.**

You can access the root folder of the repository by entering the command below:

      cd edb-ansible

**This step does not automatically make the 'edb_postgres' collection available to your playbooks.**


Hosts file content
----------------

Content of the hosts.yml file:

      servers:
        pem-server:
          node_type: pemserver
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
        primary1:
          node_type: primary
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          pem_agent: True
        standby11:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          pem_agent: True
        standby12:
          node_type: standby
          public_ip: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          pem_agent: True



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
        - edb_devops.postgres

      vars_files:
        - hosts.yml

      # Internal processing purposes only
      pre_tasks:
        # Define or re-define any variables previously assigned
        - name: Initialize the user defined variables
          set_fact:
            # 'Centos7' or 'RHEL7'
            os: "Centos7"
            # 'PG' or 'EPAS'
            pg_type: "EPAS"
            pg_data: "/data/pgdata"
            pg_wal: "/data/pg_wal"
            # Ensure you enter your credentials when utilizing EDB custom repositories
            yum_username: ""
            yum_password: ""
            standby_quorum_type: "ANY" # Quorum type can be ANY or FIRST
            
      roles:
       - setup_repo
       - install_dbserver
       - init_dbserver
       - setup_replication
       - setup_efm
       - setup_pem
 

**Defining and adding variables can be done in the set_fact of the pre-tasks.**

**You can customize the above example to install 'Postgres', 'EPAS', 'EFM' or PEM or limit what roles you would like to execute: 'setup_repo', 'install_dbserver', 'init_dbserver', 'setup_replication' or 'setup_efm' or setup_pem.**


Default user and passwords
----------------
The following will occur should a password not be provided for the following accounts:

```
* pg_superuser
* pg_replication_user
* pg_efm_user
* pg_pem_agent_user
* pg_pem_admin_user
```

**Note:**

* The `~/.edb` folder and contained files are secured by assigning the permissions to `user` executing the playbook.
* A password of 20 characters will be automatically created under: `~/.edb` folder. 
* The naming convention for the password file is: `<username>_pass`



Playbook examples:
----------------

Examples of utilizing the playbooks for installing: Postgres, EnterpriseDB Postgres Advanced Server, Centos7 or RHEL7 are provided and located within the ```playbook-examples``` directory.



Executing the playbook:
----------------

Centos7/8

      ansible-playbook -private-key=<yourprivatekey> playbook.yml -u centos

RHEL7/8

       ansible-playbook -private-key=<yourprivatekey> playbook.yml -u ec2-user




Database Engines Supported
----------------

Community Postgresql
----------------

| Distribution | 10 | 11 | 12 |13|
| ------------------------- |:--:|:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian | :x: | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: | :x: |

Enterprise DB Postgresql Advanced Server
----------------

| Distribution | 10 | 11 | 12 |13|
| ------------------------- |:--:|:--:|:--:|:--:|
| Centos 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Red Hat Linux 7 | :white_check_mark:| :white_check_mark:| :white_check_mark:| :white_check_mark:|
| Debian | :x: | :x: | :x: | :x: |
| Ubuntu | :x: | :x: | :x: | :x: |
| SLES | :x: | :x: | :x: | :x: |

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
