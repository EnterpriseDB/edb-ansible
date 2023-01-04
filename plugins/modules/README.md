# Modules

## edb_devops.edb_postgres.linesinfile

This in-house Ansible module is intended to provide better performance than
the built-in `lineinfile` module when multiple lines must be managed.

Instead of using a loop, with `linesinfile`, we can pass an array of lines.
This way, the module is executed only once, whatever the number of managed
lines is.

Most of `lineinfile`'s attributes are supported and work in the same way as
they work in `lineinfile`: `line`, `regexp`, `insertafter`, `insertbefore`,
`state`, `backrefs`, `firstmatch`, `create`, `owner`, `group`, `mode`.

A few attributes are not supported: `backup` and `search_string`.

Example:
```yaml
- name: Manage lines in file1.txt
  edb_devops.edb_postgres.linesinfile:
    path: file1.txt
    lines:
      - regexp: "Line [0-9]+.*"
        state: absent
      - line: "Test..."
        insertafter: "^Bar.*"
        firstmatch: true
      - line: "Line present"
        state: present
        insertbefore: "BOF"
      - line: "Bar"
      - line: 'Has been \1'
        regexp: '.*(replaced).*'
        backrefs: true
    group: staff
    owner: julien
    mode: 0600
    create: true
```
