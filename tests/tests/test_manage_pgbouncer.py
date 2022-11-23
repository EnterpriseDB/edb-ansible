from conftest import (
    get_pg_type,
    get_pgbouncer,
    get_pgbouncer_auth_file,
    get_pgbouncer_pid_file,
    get_primary,
    load_ansible_vars,
)


def test_manage_pgbouncer_test_db():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars["pgbouncer_auth_user_list"][0]["username"]
    pgbouncer_password = ansible_vars["pgbouncer_auth_user_list"][0]["password"]
    pgbouncer_port = ansible_vars["pgbouncer_listen_port"]
    test_db = ansible_vars["pgbouncer_databases_list"][0]["dbname"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgbouncer_address = get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "SHOW databases"
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s'  #  noqa
            % (
                pgbouncer_password,
                pgbouncer_user,
                address,
                pgbouncer_port,
                query,
                test_db,
            )
        )
        result = cmd.stdout.strip()

    assert len(result) > 0, "pgbouncer test_db not created sucessfully."


def test_manage_pgbouncer_pid_file():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars["pgbouncer_auth_user_list"][0]["username"]
    pgbouncer_password = ansible_vars["pgbouncer_auth_user_list"][0]["password"]
    pgbouncer_port = ansible_vars["pgbouncer_listen_port"]
    pgbouncer_pid_file = get_pgbouncer_pid_file()

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgbouncer_address = get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "SHOW config"
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s'
            % (
                pgbouncer_password,
                pgbouncer_user,
                address,
                pgbouncer_port,
                query,
                "pidfile",
            )
        )
        result = cmd.stdout.strip()

    assert (
        pgbouncer_pid_file in result
    ), "pgbouncer pid file was not configured properly."


def test_manage_pgbouncer_auth_file():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars["pgbouncer_auth_user_list"][0]["username"]
    pgbouncer_password = ansible_vars["pgbouncer_auth_user_list"][0]["password"]
    pgbouncer_port = ansible_vars["pgbouncer_listen_port"]
    pgbouncer_auth_file = get_pgbouncer_auth_file()

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgbouncer_address = get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "SHOW config"
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s'
            % (
                pgbouncer_password,
                pgbouncer_user,
                address,
                pgbouncer_port,
                query,
                "auth_file",
            )
        )
        result = cmd.stdout.strip()

    assert (
        pgbouncer_auth_file in result
    ), "pgbouncer auth file was not configured properly."


def test_manage_pgbouncer_users():
    ansible_vars = load_ansible_vars()
    pgbouncer_user = ansible_vars["pgbouncer_auth_user_list"][0]["username"]
    pgbouncer_password = ansible_vars["pgbouncer_auth_user_list"][0]["password"]
    pgbouncer_port = ansible_vars["pgbouncer_listen_port"]

    pg_user = "postgres"

    if get_pg_type() == "EPAS":
        pg_user = "enterprisedb"

    pgbouncer_address = get_pgbouncer()[0]
    address = str(pgbouncer_address).strip("<>").split("//")[1]
    host = get_primary()

    with host.sudo(pg_user):
        query = "SHOW users"
        cmd = host.run(
            'PGPASSWORD=%s psql -At -U %s -h %s -p %s -c "%s" pgbouncer | grep %s'
            % (
                pgbouncer_password,
                pgbouncer_user,
                address,
                pgbouncer_port,
                query,
                "pgbouncer",
            )
        )
        result = cmd.stdout.strip()
    result = result.split("\n")
    assert len(result) == 2, "pgbouncer users have not been successfully created."
