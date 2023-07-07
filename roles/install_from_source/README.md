# install_from_source

This Ansible Galaxy Role downloads and installs software from source.  It is
currently the user's responsibility to ensure required packages are installed
in order to build the software that is being installed.

## Requirements

The only dependencies required for this Ansible galaxy role are:

  1. Ansible

## Role variables

When executing the role via Ansible these are the required variables:

  * ***src_type***

  Defines what is being downloaded:

    * ***git*** - Use a git repository.
    * ***local*** - Copy a directory from the local system.
    * ***tarball*** - An archived file containing the source.

  * ***url***

  The URL pointing to the location of the source to be downloaded.  This is
  simply a path when **src_type** is `local`.

When executing the role via Ansible these are the optional variables:

  * ***configure_args***

  A list of additional flags to use with the `configure` command.

  * ***make_args***

  A list of additional flags to use with the `make` command when compiling.

  * ***srcdir***

  Directory to unpack source, default: `/usr/local/src`

  * ***tmpdir***

  Directory to save downloaded files, default: `/tmp`

## Dependencies

This role does not have any dependencies on any other roles.

## Example Playbook

### How to include into your Playbook

Below is an example of how to include this role to install PostgreSQL v9.6.24
from a source tarball:

```yaml
---
- hosts: all
  name: test install from source
  become: true
  gather_facts: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize variables
      set_fact:
        configure_args:
          - --prefix=/usr/pgsql-9.6
          - --without-readline
          - --without-zlib
        make_args:
          - world
        src_type: "tarball"
        url: "https://ftp.postgresql.org/pub/source/v9.6.24/postgresql-9.6.24.tar.bz2"

  roles:
    - install_from_source
```

Below is an example of how to include this role to install PostgreSQL v9.6.24
from a source tarball:

```
---
- hosts: all
  name: test install from source
  become: true
  gather_facts: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize variables
      set_fact:
        configure_args:
          - --prefix=/usr/pgsql-git
          - --without-icu
          - --without-readline
          - --without-zlib
        make_args:
          - world
        src_type: "git"
        url: "https://github.com/postgres/postgres.git"

  roles:
    - install_from_source
```

Below is an example of how to include this role to install a local postgres
source directory:

```
---
- hosts: all
  name: test install from source
  become: true
  gather_facts: true

  collections:
    - edb_devops.edb_postgres

  pre_tasks:
    - name: Initialize variables
      set_fact:
        configure_args:
          - --prefix=/usr/pgsql
          - --without-icu
          - --without-readline
          - --without-zlib
        make_args:
          - world
        src_type: "local"
        url: "/tmp/postgres"

  roles:
    - install_from_source
```

Defining variables is done in the `set_fact` of the `pre_tasks`.

## License

BSD

## Author information

Author:

  * Mark Wong
  * EDB Postgres
  * DevOps
  * edb-devops@enterprisedb www.enterprisedb.com
