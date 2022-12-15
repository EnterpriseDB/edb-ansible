# setup_repo

This Ansible Role sets up and configures the repositories from which
packages will be retrieved for any PostgresSQL installations.

**Not all Distribution or versions are supported on all the operating systems
available.**

For more details refer to the
[Database engines supported](#database-engines-supported) section.

**Note:**
Should there be a need to install and/or configure a PostgreSQL  Cluster
you can utilize the **install_dbserver** role.

**The ansible playbook must be executed under an account that has full
privileges.**

## Requirements

The only dependency required for this ansible galaxy role is:

1. Ansible

## Role variables

When executing the role via Ansible these are the required variables:

- **pg_version**

<<<<<<< Updated upstream
  Postgres Versions supported are: `14.0`,`14.1`,`14.2`,`14.3`,`14.3`,`14.5`,`14.6`
=======
  Postgres Versions supported are: `14.0`, `14.1`, `14.2`, `14.3`,`14.3`, `14.5`, `14.6`
>>>>>>> Stashed changes

- **pg_type**

  Database Engine supported are: `PG`

- **yum_additional_repos**

List of additional YUM repositories. List items are dictionnaries:

- _name_ - Repository name
- _description_ - Repository description
- _baseurl_ - Repository URL
- _gpgkey_ - GPG key locatio. Default: `None`
- _gpgcheck_ - Enable package signature checking with GPG. Default: `false`

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

- **apt_additional_repos**

List of additional APT repositories. List items are dictionnaries:

- _repo_ - Debian repository connection string
- _filename_ - Repository file name on disk: `<filename>.list`

The rest of the variables can be configured and are available in the:

- [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

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

Below is an example of how to include the `setup_repo` role for
setting up repositories access to PostgreSQL packages in version 14:

```yaml
---
- hosts: all
  name: Setup PostgreSQL Repositories
  become: yes
  gather_facts: yes

  collections:
    - hypersql_devops.postgres

  pre_tasks:
    - name: Initialize the user defined variables
      set_fact:
        pg_version: 14.6
        pg_type: "PG"

  roles:
    - setup_repo
```

Defining and adding variables is done in the `set_fact` of the `pre_tasks`.

All the variables are available at:

- [roles/setup_repo/defaults/main.yml](./defaults/main.yml)

## Database engines supported

### PostgreSQL

| Distribution                      |               14 |
| --------------------------------- |:----------------:|
| CentOS 7                          |:white_check_mark:|
| CentOS 8                          |:white_check_mark:|
| Ubuntu 20.04 LTS (Focal) - x86_64 |:white_check_mark:|

- :white_check_mark: - Tested and supported

## Playbook execution examples

```bash
# To setup community repos
$ ansible-playbook playbook.yml \
  -u <ssh-user> \
  --private-key <ssh-private-key> \
  --extra-vars="pg_type=PG pg_version=14.6"
```

## License

BSD

## Author information

Author:
  * [Sang Myeung Lee](https://github.com/sungmu1)

Original Author:
  * Doug Ortiz
  * Vibhor Kumar (Co-Author)
  * Julien Tachoires (Co-Author)
  
