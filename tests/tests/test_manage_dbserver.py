import pytest

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_version,
    get_pg_type,
    get_pg_unix_socket_dir,
    get_primary,
)

def test_manage_dbserver_files():
    pg_user = 'postgres'
    pg_group = 'postgres'
    profile_path = 'pgsql'
    profile_prefix = 'pgsql'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'
        profile_path = 'edb'
        profile_prefix = 'enterprisedb'
    
    host = get_primary()

    #Testing if '.psqlrc' file was created

    assert host.file('/var/lib/%s/.psqlrc' % profile_path).exists, \
        ".psqlrc does not exist"
    
    assert host.file('/var/lib/%s/.psqlrc' % profile_path).user == pg_user, \
        ".psqlrc is not owned by postgres"
    
    assert host.file('/var/lib/%s/.psqlrc' % profile_path).group == pg_group, \
        ".psqlrc group is not in postgres"

    #Testing if shell profile was created

    assert host.file('/var/lib/%s/.%s_profile' % (profile_path, profile_prefix)).exists, \
        "%s_profile does not exist" % pg_user

    assert host.file('/var/lib/%s/.%s_profile' % (profile_path, profile_prefix)).user == pg_user, \
        "%s_profile is not owned by postgres" % pg_user
    
    assert host.file('/var/lib/%s/.%s_profile' % (profile_path, profile_prefix)).group == pg_group, \
        "%s_profile group is not in postgres" % pg_user
    
def test_manage_dbserver_conf_params():
    ansible_vars = load_ansible_vars()
    pg_conf_param = ansible_vars['pg_conf_param']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Show %s" % pg_conf_param
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
    "Database parameter %s does not exist" % pg_conf_param

def test_manage_dbserver_pg_slots():
    ansible_vars = load_ansible_vars()
    pg_slot = ansible_vars['pg_slot']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots WHERE slot_name = '%s'" % pg_slot
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
    "Replication slots %s does not exist" % pg_slot

def test_manage_dbserver_pg_extension():
    ansible_vars = load_ansible_vars()
    pg_extension = ansible_vars['pg_extension']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_extension WHERE extname = '%s'" % pg_extension
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
    "PG extension %s does not exist" % pg_extension

def test_manage_dbserver_pg_extension():
    ansible_vars = load_ansible_vars()
    pg_extension = ansible_vars['pg_extension']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_extension WHERE extname = '%s'" % pg_extension
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
    "PG extension %s does not exist" % pg_extension

def test_manage_dbserver_query():
    ansible_vars = load_ansible_vars()
    pg_query_table = ansible_vars['pg_query_table']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    
    with host.sudo(pg_user):
        query = "Select * from pg_tables where tablename = '%s'" % pg_query_table
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, \
    "Query wwas not succesfully executed" % pg_query_table


