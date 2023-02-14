# Common

This is a role that contains common utility tasks shared by roles in **tmax_opensql.postgres**. Some tasks are collection independent, but most of them are very much dependent. Also, if the role is activated by "roles" option in playbook, it will fail (deliberately) because this role is meant to be just a group of individual tasks.

## Requirements

Just Ansible

## Role Variables

All the variables are available at:

- [roles/common/defaults/main.yml](./defaults/main.yml)
- [roles/common/vars/main.yml](./vars/main.yml)

## Dependencies

No Dependencies

## Example Playbook

As it was mentioned earlier, this role should be used by importing individual tasks in it. For example, _check_required_variables_ task is used in _manage_dbserver_ role as below:

```yml
# Check required variables
- name: Check required variables for this role
  include_role:
    name: common
    tasks_from: check_required_variables
  vars:
    required_variables:
      - pg_type
      - pg_version
```

## License

BSD

## Author Information

- [Sung Woo Chang](https://github.com/dbxpert)
- [Sang Myeung Lee](https://github.com/sungmu1)
