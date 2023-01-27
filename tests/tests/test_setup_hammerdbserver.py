import pytest
import os

from conftest import (
    load_ansible_vars,
    get_os_version,
    get_hammerdb,
    os_family,
)

def test_setup_hammerdbserver_dir():
    ansible_vars = load_ansible_vars()
    hammerdb = ansible_vars['hammerdb']
    host = get_hammerdb()[0]
    
    assert host.file(hammerdb).exists, \
        "HammerDB wasn't sucessfully installed"

def test_setup_hammerdbserver_install_file():
    ansible_vars = load_ansible_vars()
    hammerdb_version = ansible_vars['hammerdb_version']
    host = get_hammerdb()[0]

    if os_family() == 'RedHat':
        ext = 'RHEL%s' % get_os_version()
    else:
        ext = 'Linux'
    
    assert host.file('HammerDB-%s-%s.tar.gz' % (hammerdb_version, ext)).exists, \
        "HammerDB install file wasn't downloaded"

