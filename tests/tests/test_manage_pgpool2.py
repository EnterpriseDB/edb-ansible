import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pgpool2,
    get_pg_version,
    get_primary
)

def test_manage_pgpool_pcp_user():
    #PCP commands only available for pg-pool-4.3 which is only available for EPAS
    if get_pg_type() == 'PG':
        pytest.skip()

    ansible_vars = load_ansible_vars()
    pcp_user = ansible_vars['pcp_users'][0]['name']
    pcp_pass = ansible_vars['pcp_users'][0]['pass']
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_pgpool2()[0]

    with host.sudo(pg_user):
        cmd = host.run("touch ~/.pcppass")
        cmd = host.run("echo 'localhost:9898:%s:%s' >> ~/.pcppass" % (pcp_user, pcp_pass))
        cmd = host.run("chmod 600 ~/.pcppass ")
        cmd = host.run("pcp_node_info -U %s -h localhost -w" % pcp_user)
        result = cmd.stdout.strip()
        
    assert len(result) > 0, \
        "pcp command succesfully works"

def test_manage_pgpool_pcp_node_count():
    #PCP commands only available for pg-pool-4.3 which is only available for EPAS
    if get_pg_type() == 'PG':
        pytest.skip()

    ansible_vars = load_ansible_vars()
    pcp_user = ansible_vars['pcp_users'][0]['name']
    pcp_pass = ansible_vars['pcp_users'][0]['pass']
    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    host = get_pgpool2()[0]

    with host.sudo(pg_user):
        cmd = host.run("pcp_node_count -U %s -h localhost -w" % pcp_user)
        result = cmd.stdout.strip()
        
    assert result == '1', \
        "Database node count is not equal to 1"

def test_manage_pgpool_test_user():
    ansible_vars = load_ansible_vars()
    pgpool2_user = ansible_vars['pgpool2_users'][0]['name']
    pgpool2_password = ansible_vars['pgpool2_users'][0]['pass']
    pgpool2_port = ansible_vars['pgpool2_port']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    pgpool2_address= get_pgpool2()[0]
    address = str(pgpool2_address).strip("<>").split('//')[1]
    host = get_primary()
    
    with host.sudo(pg_user):
        query = "Select usename from pg_user where usename = '%s'" % pgpool2_user
        cmd = host.run('PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" postgres' % (pgpool2_password, 
                                                                                            pgpool2_user, 
                                                                                            address, 
                                                                                            pgpool2_port, 
                                                                                            query))
        result = cmd.stdout.strip().split('\n')

    assert len(result) == 1, \
        "test user was not created sucessfully."

def test_manage_pgpool_pcp_socket():
    ansible_vars = load_ansible_vars()
    pgpool2_user = ansible_vars['pgpool2_users'][0]['name']
    pgpool2_password = ansible_vars['pgpool2_users'][0]['pass']
    pgpool2_port = ansible_vars['pgpool2_port']

    pg_user = 'postgres'
    pg_group = 'postgres'

    if get_pg_type() == 'EPAS':
        pg_user = 'enterprisedb'
        pg_group = 'enterprisedb'

    pgpool2_address= get_pgpool2()[0]
    address = str(pgpool2_address).strip("<>").split('//')[1]
    host = get_primary()
    
    with host.sudo(pg_user):
        query = "PGPOOL SHOW pcp_socket_dir;"
        cmd = host.run("PGPASSWORD=%s psql -At -U %s -h %s -p %s -c '%s' postgres" % (pgpool2_password, 
                                                                                            pgpool2_user, 
                                                                                            address, 
                                                                                            pgpool2_port, 
                                                                                            query))
        result = cmd.stdout.strip()

    assert result == '/tmp', \
        "Load Balance is not enabled."