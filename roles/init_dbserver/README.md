# init_dbserver

This Ansible Galaxy Role Initializes Postgres or EnterpriseDB Postgresql
Advanced Server versions: 10, 11, 12, 13, 14 and 15 on instances previously configured.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the: *Database engines supported* section.

**Note:**
The role does not configure Postgres nor EnterpriseDB Postgres Advanced Server
for replication, it only installs Postgres or EnterpriseDB Postgres Advanced
Server across multiple nodes: primary and pemserver.
Should there be a need to configure a Postgres or EnterpriseDB Postgres
Advanced Server Cluster for replication you can utilize the `setup_replication`
role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependencies required for this ansible galaxy role are:

  1. Ansible
  2. `community.general` Ansible Module - Utilized when creating aditional
     users during a Postgres Install. Only on primary nodes.
  3. `edb_devops.edb_postgres` -> `setup_repo` - for repository installation
  4. `edb_devops.edb_postgres` -> `install_dbserver` - for installation of
     PostgreSQL/EPAS binaries.

## Role variables

When executing the role via ansible there are three required variables:

  * ***pg_version***

  Postgres Versions supported are: 10, 11, 12, 13, 14 and 15

  * ***pg_type***

  Database Engine supported are: PG and EPAS

With above two variables, role has the following optional variables to enable
**Transparent Data Encryption (TDE) for EPAS versions 15.0 and above**:
* ***edb_enable_tde***

Supported value is true or false. This variable informs roles to execute specific tasks related Enable TDE

* ***edb_key_unwrap_cmd***

Unwrap commad to decrypt EDB master key. User can also pass KMS using the above parameter to
EPAS for using master key for encryption. For more information, please refer to EPAS guide on TDE.
This parameter used by EDB during starting the Postgres service.

* ***edb_key_wrap_cmd***

Wrap command to encrypt EDB master key. User can also use KMS commands to get the key
and encrypt the master key to store in EPAS.

* ***edb_master_key***

This is an optional key master key parameter. Using this parameter user can pass a master key. If you don't want to use this parameter then pass radom string and ensure that your _edb_key_unwrap_cmd_ and _edb_key_wrap_cmd_ commands can get the right key from known KMS.

* ***edb_secure_master_key***

 This is an option key for encrypting _edb_master_key_ to keep it secure in EPAS. User can skip _edb_master_key_ and _edb_secure_master_key_ both by ensuring that edb_key_unwrap_cmd_ and _edb_key_wrap_cmd_ commands can get the right key from known KMS.


These and other variables can be assigned in the `pre_tasks` definition of the
section: *How to include the `init_dbserver` role in your Playbook*

The rest of the variables can be configured and are available in the:

  * [roles/init_dbserver/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  * [roles/init_dbserver/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/init_dbserver/vars/PG_Debian.yml](./vars/PG_Debian.yml)
  * [roles/init_dbserver/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)

## Dependencies

The `init_dbserver` role does not have any dependencies on any other roles.

## Example Playbook

### Inventory file content

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    pemserver:
      hosts:
        pemserver1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
    primary:
      hosts:
        primary1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
    standby:
      hosts:
        standby1:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: synchronous
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
        standby2:
          ansible_host: xxx.xxx.xxx.xxx
          private_ip: xxx.xxx.xxx.xxx
          upstream_node_private_ip: xxx.xxx.xxx.xxx
          replication_type: asynchronous
          pem_agent: true
          pem_server_private_ip: xxx.xxx.xxx.xxx
```

### How to include the `init_dbserver` role in your Playbook

Below is an example of how to include the `init_dbserver` role:

```yaml
---
- hosts: primary, pemserver
  name: Initialize Postgres instances
  become: yes
  gather_facts: yes
  any_errors_fatal: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: install_dbserver
      when: "'install_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
    - role: initdb_dbserver
      when: "'init_dbserver' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/init_dbserver/defaults/main.yml](./defaults/main.yml)
  * [roles/init_dbserver/vars/EPAS_RedHat.yml](./vars/EPAS_RedHat.yml)
  * [roles/init_dbserver/vars/EPAS_Debian.yml](./vars/EPAS_Debian.yml)
  * [roles/init_dbserver/vars/PG_RedHat.yml](./vars/PG_RedHat.yml)
  * [roles/init_dbserver/vars/PG_Debian.yml](./vars/PG_Debian.yml)
  * [roles/init_dbserver/vars/edb-ssl.yml](./vars/edb-ssl.yml)

## Database engines supported

### PostgreSQL

| Distribution                      |               10 |               11 |               12 |               13 |               14 |               15 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| AlmaLinux8                        |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
### EnterpriseDB Postgres Advanced Server

| Distribution                      |               10 |               11 |               12 |               13 |               14 |               15 |
| --------------------------------- |:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|:----------------:|
| CentOS 7                          |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 7                   |:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| RockyLinux 8                      |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Red Hat Linux 8                   |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| AlmaLinux8                        |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |               :x:|               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 9 (Stretch) - x86_64       |               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|
| Debian 10 (Buster) - x86_64       |               :x:|               :x:|:white_check_mark:|:white_check_mark:|:white_check_mark:|:white_check_mark:|

- :white_check_mark: - Tested and supported

## Playbook execution examples

```bash
# To deploy community Postgres version 13 with the user centos
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u centos \
  --private-key <key.pem> \
  --extra-vars="pg_version=13 pg_type=PG"
```
```bash
# To deploy EPAS version 12 with the user ec2-user
$ ansible-playbook playbook.yml \
  -i inventory.yml \
  -u ec2-user \
  --private-key <key.pem> \
  --extra-vars="pg_version=12 pg_type=EPAS"
```

## License

BSD

## Author information

Author:

  * Doug Ortiz
  * Julien Tachoires
  * Vibhor Kumar
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
