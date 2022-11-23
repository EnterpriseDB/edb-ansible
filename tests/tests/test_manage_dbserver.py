from conftest import (
    get_pg_profile_dir,
    get_pg_type,
    get_pg_unix_socket_dir,
    get_primary,
    load_ansible_vars,
)


def test_manage_dbserver_files():
    ansible_vars = load_ansible_vars()
    pg_user = "postgres"
    pg_group = "postgres"
    pg_profile_path = get_pg_profile_dir()
    pg_sql_script = ansible_vars["pg_sql_scripts"][0]["file_path"]
    profile_prefix = "pgsql"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"
        pg_group = "enterprisedb"
        profile_prefix = "enterprisedb"

    host = get_primary()

    # Testing if '.psqlrc' file was created properly

    assert host.file("%s/.psqlrc" % pg_profile_path).exists, ".psqlrc does not exist"

    assert host.file("%s/.psqlrc" % pg_profile_path).user == pg_user, (
        ".psqlrc is not owned by %s" % pg_user
    )

    assert host.file("%s/.psqlrc" % pg_profile_path).group == pg_group, (
        ".psqlrc group is not in %s" % pg_user
    )

    # Testing if shell profile was created properly

    assert host.file("%s/.%s_profile" % (pg_profile_path, profile_prefix)).exists, (
        "%s_profile does not exist" % pg_user
    )

    assert (
        host.file("%s/.%s_profile" % (pg_profile_path, profile_prefix)).user == pg_user
    ), "%s_profile is not owned by %s" % (pg_user, pg_user)

    assert (
        host.file("%s/.%s_profile" % (pg_profile_path, profile_prefix)).group
        == pg_group
    ), "%s_profile group is not in %s" % (pg_user, pg_user)

    # Testing if '.pgpass' file was created properly

    assert host.file("%s/.pgpass" % pg_profile_path).exists, ".pgpass does not exist"

    assert host.file("%s/.pgpass" % pg_profile_path).user == pg_user, (
        ".psqlrc is not owned by %s" % pg_user
    )

    assert host.file("%s/.pgpass" % pg_profile_path).group == pg_group, (
        ".psqlrc group is not in %s" % pg_group
    )

    assert host.file("%s/.pgpass" % pg_profile_path).exists, ".pgpass does not exist"

    # Testing if files were properly copied over

    assert host.file(
        "%s" % pg_sql_script
    ).exists, "File(s) were not properly copied over"


def test_manage_dbserver_create_user():
    ansible_vars = load_ansible_vars()
    pg_user = "postgres"
    pg_created_user = ansible_vars["pg_users"][0]["name"]

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()
    with host.sudo(pg_user):
        query = "Select * from pg_user WHERE usename='%s'" % pg_created_user
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "User was not sucessfully created."


def test_manage_dbserver_sql_script():
    ansible_vars = load_ansible_vars()
    pg_user = "postgres"
    pg_sql_script = ansible_vars["pg_sql_scripts"][0]["file_path"]
    pg_script_table = ansible_vars["pg_script_table"]

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        cmd = host.run("cat %s" % pg_sql_script)
        query = cmd.stdout.strip()
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        query = "Select * from pg_tables WHERE tablename = '%s'" % pg_script_table
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "SQL scripts were not succesfully executed"


def test_manage_dbserver_hba_file():
    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Show hba_file"
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    cmd = host.run("grep postgres %s" % result)
    result = cmd.stdout.strip()

    assert len(result) > 0, "pg_hba.conf file was not sucessfully modified"


def test_manage_dbserver_conf_params():
    ansible_vars = load_ansible_vars()
    pg_conf_param = ansible_vars["pg_postgres_conf_params"][0]["name"]
    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Show %s" % pg_conf_param
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "Database parameter %s does not exist" % pg_conf_param


def test_manage_dbserver_pg_slots():
    ansible_vars = load_ansible_vars()
    pg_slot = ansible_vars["pg_slots"][0]["name"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_replication_slots WHERE slot_name = '%s'" % pg_slot
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "Replication slots %s does not exist" % pg_slot


def test_manage_dbserver_pg_extension():
    ansible_vars = load_ansible_vars()
    pg_extension = ansible_vars["pg_extensions"][0]["name"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_extension WHERE extname = '%s'" % pg_extension
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "PG extension %s does not exist" % pg_extension


def test_manage_dbserver_pg_grant_roles():
    ansible_vars = load_ansible_vars()
    pg_role = ansible_vars["pg_grant_roles"][0]["role"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = (
            "Select rolname FROM pg_roles WHERE pg_has_role('%s', oid, 'member') AND rolname = '%s'"
            % (pg_user, pg_role)
        )
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "User %s has not been granted the %s role" % (
        pg_user,
        pg_role,
    )


def test_manage_dbserver_query():
    ansible_vars = load_ansible_vars()
    pg_query_table = ansible_vars["pg_query_table"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_tables WHERE tablename = '%s'" % pg_query_table
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "Query wwas not succesfully executed" % pg_query_table


def test_manage_dbserver_database():
    ansible_vars = load_ansible_vars()
    pg_database = ansible_vars["pg_databases"][0]["name"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    host = get_primary()
    socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "Select * from pg_database WHERE datname = '%s'" % pg_database
        cmd = host.run('psql -At -h %s -c "%s" postgres' % (socket_dir, query))
        result = cmd.stdout.strip()

    assert len(result) > 0, "Query was not succesfully executed" % pg_database
