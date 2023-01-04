#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)

import errno
import fcntl
import os
import re
import time
import tempfile

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native, to_text


__metaclass__ = type

DOCUMENTATION = r'''
---
module: linesinfile
short_description: Manage a list of lines in text files
description:
  - This module ensures a list of lines is in a file, or replace an
    existing line using a back-referenced regular expression.
  - This module is intended to replace the usage of the lineinfile module when multiple lines are passed.
options:
  path:
    description:
      - The file to modify.
    type: path
    required: true
    aliases: [ dest, destfile, name ]
  regexp:
    description:
      - The regular expression to look for in every line of the file.
      - For C(state=present), the pattern to replace if found. Only the last line found will be replaced.
      - For C(state=absent), the pattern of the line(s) to remove.
      - If the regular expression is not matched, the line will be
        added to the file in keeping with C(insertbefore) or C(insertafter)
        settings.
      - When modifying a line the regexp should typically match both the initial state of
        the line as well as its state after replacement by C(line) to ensure idempotence.
      - Uses Python regular expressions. See U(https://docs.python.org/3/library/re.html).
    type: str
    aliases: [ regex ]
  state:
    description:
      - Whether the line should be there or not.
    type: str
    choices: [ absent, present ]
    default: present
  lines:
    description:
      - Array of lines to be managed
  lines[N].line:
    description:
      - The line to insert/replace into the file.
      - Required for C(state=present).
      - If C(backrefs) is set, may contain backreferences that will get
        expanded with the C(regexp) capture groups if the regexp matches.
    type: str
    aliases: [ value ]
  lines[N].backrefs:
    description:
      - Used with C(state=present).
      - If set, C(line) can contain backreferences (both positional and named)
        that will get populated if the C(regexp) matches.
      - This parameter changes the operation of the module slightly;
        C(insertbefore) and C(insertafter) will be ignored, and if the C(regexp)
        does not match anywhere in the file, the file will be left unchanged.
      - If the C(regexp) does match, the last matching line will be replaced by
        the expanded line parameter.
    type: bool
    default: no
  lines[N].insertafter:
    description:
      - Used with C(state=present).
      - If specified, the line will be inserted after the last match of specified regular expression.
      - If the first match is required, use(firstmatch=yes).
      - A special value is available; C(EOF) for inserting the line at the end of the file.
      - If specified regular expression has no matches, EOF will be used instead.
      - If C(insertbefore) is set, default value C(EOF) will be ignored.
      - If regular expressions are passed to both C(regexp) and C(insertafter), C(insertafter) is only honored if no match for C(regexp) is found.
      - May not be used with C(backrefs) or C(insertbefore).
    type: str
    choices: [ EOF, '*regex*' ]
    default: EOF
  lines[N].insertbefore:
    description:
      - Used with C(state=present).
      - If specified, the line will be inserted before the last match of specified regular expression.
      - If the first match is required, use C(firstmatch=yes).
      - A value is available; C(BOF) for inserting the line at the beginning of the file.
      - If specified regular expression has no matches, the line will be inserted at the end of the file.
      - If regular expressions are passed to both C(regexp) and C(insertbefore), C(insertbefore) is only honored if no match for C(regexp) is found.
      - May not be used with C(backrefs) or C(insertafter).
    type: str
    choices: [ BOF, '*regex*' ]
  lines[N].firstmatch:
    description:
      - Used with C(insertafter) or C(insertbefore).
      - If set, C(insertafter) and C(insertbefore) will work with the first line that matches the given regular expression.
    type: bool
    default: no
  create:
    description:
      - Used with C(state=present).
      - If specified, the file will be created if it does not already exist.
      - By default it will fail if the file is missing.
    type: bool
    default: no
  others:
    description:
      - All arguments accepted by the M(ansible.builtin.file) module also work here.
    type: str
author:
    - Julien Tachoires

'''

EXAMPLES = r'''
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
'''

RETURN = r'''#'''


class lopen:
    def __init__(self, module, file, mode='r'):
        self.file = file
        self.mode = mode
        self.fd = None
        self.module = module

    def __enter__(self):
        self.fd = open(self.file, self.mode)
        t = 0
        while True:
            t += 1

            if t > 1000:
                # Raise an error after 100 seconds if we can not open the
                # file because of an exclusive lock is held by another process.
                self.module.fail_json(
                    rc=256,
                    msg="Unable to obtain an exclusive lock on %s" % self.file
                )

            try:
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self.fd
            except IOError as e:
                # Raise on unrelated IOErrors
                if e.errno != errno.EAGAIN:
                    raise
                else:
                    time.sleep(0.1)

    def __exit__(self, exc_type, exc_value, traceback):
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        self.fd.close()


def write_changes(module, buffer, dest):
    # Write buffer content into a temporary file and then make an atomic move
    tmpfd, tmpfile = tempfile.mkstemp(dir=module.tmpdir)
    with os.fdopen(tmpfd, 'wb') as f:
        f.writelines(buffer)

    module.atomic_move(
        tmpfile,
        to_native(
            os.path.realpath(
                to_bytes(dest, errors='surrogate_or_strict')
            ),
            errors='surrogate_or_strict'
        ),
        unsafe_writes=False
    )


def check_file_attrs(module, changed, message, diff):
    file_args = module.load_file_common_arguments(module.params)
    if module.set_fs_attributes_if_different(file_args, False, diff=diff):

        if changed:
            message += " and "
        changed = True
        message += "ownership, perms or SE linux context changed"

    return message, changed


def create_file(module, dest):
    if os.path.exists(dest):
        return
    try:
        with open(dest, 'w') as f:
            f.write('')
    except Exception:
        module.fail_json(rc=256, msg="Unable to create the file %s" % dest)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True),
            lines=dict(type='list', required=True),
            create=dict(type='bool', default=False),
        ),
        add_file_common_args=True,
        supports_check_mode=True,
    )

    path = module.params['path']
    create = module.params['create']

    b_path = to_bytes(path, errors='surrogate_or_strict')
    if os.path.isdir(b_path):
        module.fail_json(rc=256, msg='Path %s is a directory !' % path)

    changed = False
    msg = ''
    diff = {
        'before': '',
        'after': '',
        'before_header': '%s (content)' % path,
        'after_header': '%s (content)' % path
    }
    counters = {
        'added': 0,
        'replaced': 0,
        'removed': 0
    }

    if create:
        create_file(module, path)

    # Open the file in read only with an exclusive lock just to be sure no
    # changes can be made by any other process while we are working on this
    # file.
    with lopen(module, b_path, 'r') as f:
        # Load file content into the buffer as a list of bytes
        buffer = [to_bytes(cl, errors='surrogate_or_strict')
                  for cl in f.readlines()]

        if module._diff:
            diff['before'] = to_native(b''.join(buffer))

        # Loop through each given line
        for line in module.params['lines']:
            l_state = line.get('state', 'present')
            l_regexp = line.get('regexp', None)
            l_insertafter = line.get('insertafter', 'EOF')
            l_insertbefore = line.get('insertbefore', None)
            l_line = line.get('line', None)
            l_backrefs = line.get('backrefs', False)
            l_firstmatch = line.get('firstmatch', False)

            if l_state == 'present' and not l_line:
                module.fail_json(rc=256, msg='line attribute must be set')

            if l_insertafter != 'EOF' and l_insertbefore is not None:
                module.fail_json(
                    rc=256,
                    msg='insertafter and insertbefore are mutually exclusive'
                )

            l_regexp = re.compile(l_regexp) if l_regexp else None

            l_insertafter_re = None
            l_insertbefore_re = None
            if l_insertafter != 'EOF':
                l_insertafter_re = re.compile(l_insertafter)
            if l_insertbefore != 'BOF' and l_insertbefore is not None:
                l_insertbefore_re = re.compile(l_insertbefore)

            if l_line:
                # Convert it to bytes
                l_line = to_bytes(l_line, errors='surrogate_or_strict')

            regexp_idxs = []
            insertafter_idxs = []
            insertbefore_idxs = []
            equal_idxs = []
            content = l_line

            # Line number
            line_no = -1

            for buffer_line in buffer:
                line_no += 1
                buffer_line = buffer_line.rstrip(to_bytes('\r\n'))

                # Let's find if the current line (buffer_line) and the input
                # line are matching.
                if l_regexp:
                    match = l_regexp.search(to_text(buffer_line))
                    if match:
                        if l_backrefs:
                            content = to_bytes(match.expand(to_text(l_line)))
                        regexp_idxs.append(line_no)
                        continue

                if l_insertafter_re and l_insertafter_re.match(to_text(buffer_line)):  # noqa
                    insertafter_idxs.append(line_no)
                    continue

                if l_insertbefore_re and l_insertbefore_re.match(to_text(buffer_line)):  # noqa
                    insertbefore_idxs.append(line_no)
                    continue

                if not l_regexp and buffer_line == l_line:
                    equal_idxs.append(line_no)

            # Apply the change
            if l_state == 'absent':
                if l_regexp:
                    regexp_idxs.reverse()
                    for idx in regexp_idxs:
                        del buffer[idx]
                        counters['removed'] += 1
                        changed = True
                else:
                    equal_idxs.reverse()
                    for idx in equal_idxs:
                        del buffer[idx]
                        counters['removed'] += 1
                        changed = True

            if l_state == 'present':
                # Not found, then append the line to the end. If insertbefore
                # is set to BOF, then the line is inserted at the beginning of
                # the file.
                if len(equal_idxs) == 0 and len(regexp_idxs) == 0 \
                        and len(insertafter_idxs) == 0 \
                        and len(insertbefore_idxs) == 0:
                    if l_insertbefore == 'BOF':
                        buffer.insert(0, content + to_bytes('\n'))
                    else:
                        buffer.append(content + to_bytes('\n'))
                    counters['added'] += 1
                    changed = True
                # Match based on regexp
                elif len(regexp_idxs) > 0:
                    buffer[regexp_idxs[-1]] = content + to_bytes('\n')
                    counters['replaced'] += 1
                    changed = True
                # Match based on insertbefore
                elif len(insertbefore_idxs) > 0:
                    if l_firstmatch:
                        p = insertbefore_idxs[0]
                    else:
                        p = insertbefore_idxs[-1]
                    if buffer[p].rstrip(to_bytes('\r\n')) != content:
                        buffer.insert(p, content + to_bytes('\n'))
                        counters['added'] += 1
                        changed = True
                # Match base on insertfater
                elif len(insertafter_idxs) > 0:
                    if l_firstmatch:
                        p = insertafter_idxs[0] + 1
                    else:
                        p = insertafter_idxs[-1] + 1
                    if p >= len(buffer):
                        buffer.insert(p, content + to_bytes('\n'))
                        counters['added'] += 1
                        changed = True
                    elif buffer[p].rstrip(to_bytes('\r\n')) != content:
                        buffer.insert(p, content + to_bytes('\n'))
                        counters['added'] += 1
                        changed = True

        if changed and not module.check_mode:
            write_changes(module, buffer, path)

    if module._diff:
        diff['after'] = to_native(b''.join(buffer))

    msg = '%s line(s) added' % counters['added']
    msg += ', %s line(s) removed' % counters['removed']
    msg += ', %s line(s) replaced' % counters['replaced']

    attr_diff = {}
    if not module.check_mode:
        msg, changed = check_file_attrs(module, changed, msg, attr_diff)

    attr_diff['before_header'] = '%s (file attributes)' % path
    attr_diff['after_header'] = '%s (file attributes)' % path

    difflist = [diff, attr_diff]
    found = sum([v for k, v in counters.items()])

    module.exit_json(changed=changed, found=found, msg=msg, diff=difflist)


if __name__ == '__main__':
    main()
