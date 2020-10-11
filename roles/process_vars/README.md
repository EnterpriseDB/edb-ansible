Role Name
=========

process_var roles processes all the variables needs for the roles in the collection. It needs to be executed first.

This role should always be called before any roles called by edb_postgres collections

Role Variables
--------------

Following are the list of variables set by this role:

PEM_SERVER_PRIVATE_IP: ""
PEM_SERVER_PUBLIC_IP: ""
PRIMARY_PRIVATE_IP: ""
PRIMARY_PUBLIC_IP: ""
PRIMARY_HOST_NAME: ""
STANDBY_NAMES: []
ALL_NODE_IPS: []
EFM_NODES_PRIVATE_IP: []
EFM_NODES_PUBLIC_IP: []
EFM_NODES_HOSTS_LIST: []
ALL_NODE_HOSTNAMES: []
ETC_HOSTS_LISTS: []


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      
      vars_files:
        - hosts.yml

      tasks:
         - name: Iterate through processing variables
           include_role:
              name: process_vars
           with_dict: "{{ servers }}"

License
-------

BSD

