# setup_repo

This Ansible Role sets up and configures the repositories from which
packages will be retrieved for any PostgresSQL or EnterpriseDB Postgres
Advanced Server installations.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the
[Database engines supported](#database-engines-supported) section.

**Note:**
Should there be a need to install and/or configure a PostgreSQL or EnterpriseDB
Postgres Advanced Server Cluster you can utilize the **install_dbserver** role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependency required for this ansible galaxy role is:

  1. Ansible

## Role variables

When executing the role via Ansible these are the required variables:

  * **pg_version**

  Postgres Versions supported are: `10`, `11`, `12`, `13`, `14` and `15`

  * **pg_type**

  Database Engine supported are: `PG` and `EPAS`

  * **enable_edb_repo**

  Configure access to EDB package repository. Default: `true`

  * **repo_username**

  Username used to access EDB package repository.
  Required when **enable_edb_repo** is set to `true` and **repo_token** isn't used.

  * **repo_password**

  Password used to access EDB package repository.
  Required when **enable_edb_repo** is set to `true` and **repo_token** isn't used.

  * **repo_token**

  EDB repository token used to access EDB package repository.
  Required when **enable_edb_repo** is set to `true` and **repo_username** and **repo_password** aren't used.

  * **repo_plan**

  Configure the EDB support plan. Plans supported are: `standard` and `enterprise`. Default: `enterprise`

  * **enable_pgdg_repo** 

  Configure access to the PGDG package repository. Default: `true`. Only set to `false` when using local repositories. 

  * **enable_epel_repo**

  Configure access to EPEL package repository on EL8 distributions. Default: `true`. Only set to `false` when using local repositories.

  * **yum_additional_repos**

  List of additional YUM repositories. List items are dictionnaries:
  * *name* - Repository name
  * *description* - Repository description
  * *baseurl* - Repository URL
  * *gpgkey* - GPG key locatio. Default: `None`
  * *gpgcheck* - Enable package signature checking with GPG. Default: `false`

  Example:
  ```yaml
        # Additional repositories
        yum_additional_repos:
          - name: "Additional Repo. 1"
            description: "Description of the repo."
            baseurl: https://my.repo.internal/CentOS$releasever-$basearch
            gpgkey: https://my.repo.internal/key.asc
            gpgcheck: true
          - name: "Local Repo"
            baseurl: file:///opt/my_local_repo
  ```

  * **apt_additional_repos**

  List of additional APT repositories. List items are dictionnaries:
  * *repo* - Debian repository connection string
  * *filename* - Repository file name on disk: `<filename>.list`


The rest of the variables can be configured and are available in the:

  * [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

## Dependencies

The `setup_repo` role does not have any dependencies on any other roles.

## Example Playbook

### Example of inventory file

Content of the `inventory.yml` file:

```yaml
---
all:
  children:
    primary:
      hosts:
        primary1:
          ansible_host: 110.0.0.1
          private_ip: 10.0.0.1
    standby:
      hosts:
        standby1:
          ansible_host: 110.0.0.2
          private_ip: 10.0.0.2
          upstream_node_private_ip: 10.0.0.1
          replication_type: synchronous
        standby2:
          ansible_host: 110.0.0.3
          private_ip: 10.0.0.3
          upstream_node_private_ip: 10.0.0.1
          replication_type: asynchronous
```

Note: don't forget to replace IP addresses.

### How to include the `setup_repo` role in your Playbook

Below is an example of how to include the `setup_repo` role for setting up
repositories access to EDB Postgres Advanced Server packages in version 14:

```yaml
---
- hosts: all
  name: Setup EPAS Repositories
  become: yes
  gather_facts: yes
  any_errors_fatal: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "EPAS"
        repo_username: "<edb-repo-username>"
        repo_password: "<edb-repo-password>"
        repo_token: "<edb-repo-token>"

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Following is another example of how to include the `setup_repo` role for
setting up repositories access to PostgreSQL packages in version 14:

```yaml
---
- hosts: all
  name: Setup PostgreSQL Repositories
  become: yes
  gather_facts: yes

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14
        pg_type: "PG"
        enable_edb_repo: false

  roles:
    - role: setup_repo
      when: "'setup_repo' in lookup('edb_devops.edb_postgres.supported_roles', wantlist=True)"
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

  * [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

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
# To setup community repos
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=PG pg_version=14 enable_edb_repo=false"
```

```bash
# To setup EDB repos
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=EPAS pg_version=14 repo_username=<edb-repo-username> repo_password=<edb-repo-password>"
# OR
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=EPAS pg_version=14 repo_token=<edb-repo-token>"
```

## License

BSD

## Author information

Author:
  * Doug Ortiz
  * Vibhor Kumar (Co-Author)
  * Julien Tachoires (Co-Author)

Contact: **edb-devops@enterprisedb.com**
