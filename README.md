postgres
=========

This Ansible Galaxy Collection sets up and configures the repositories from which packages will be retrieved for any Postgres or EnterpriseDB Postgresql Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems available.**

**The ansible playbook must be executed under an account that has full privileges.**


Dependencies
------------

The setup_repo role does not have any dependencies on any other roles.

Hosts file content
----------------

Content of the hosts.yml file:



      hosts:
        main1:
          node_type: main
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




Operating Systems Supported
----------------


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
* Collection Name: postgres 
* DevOps 
* doug.ortiz@enterprisedb.com www.enterprisedb.com
