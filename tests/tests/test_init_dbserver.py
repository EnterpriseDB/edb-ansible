from conftest import (
    get_pg_type,
    get_pg_unix_socket_dir,
    get_pg_version,
    get_primary,
    load_ansible_vars,
    os_family,
)


def test_init_dbserver_files():
    ansible_vars = load_ansible_vars()

    pg_data = ansible_vars["pg_data"]
    pg_wal = ansible_vars["pg_wal"]
    pg_user = ansible_vars["pg_owner"]
    pg_group = ansible_vars["pg_group"]

    host = get_primary()

    for pg_dir in [pg_data, pg_wal]:
        assert host.file(pg_dir).exists, "%s does not exist" % pg_dir

        assert host.file(pg_dir).is_directory, "%s is not a directory" % pg_dir

        assert host.file(pg_dir).user == pg_user, "%s is not owned by postgres" % pg_dir

        assert host.file(pg_dir).group == pg_group, "%s group is not postgres" % pg_dir

    # Test PGWAL
    assert host.file("%s/pg_wal" % pg_data).exists, "%s/pg_wal does not exist" % pg_data
    assert host.file("%s/pg_wal" % pg_data).is_symlink, (
        "%s/pg_wal is not a symlink" % pg_data
    )
    assert (
        host.file("%s/pg_wal" % pg_data).linked_to == pg_wal
    ), "%s/pg_wal is not linked to %s" % (pg_data, pg_wal)


def test_init_dbserver_service():
    host = get_primary()
    pg_version = get_pg_version()

    if os_family() == "RedHat":
        if get_pg_type() == "PG":
            service = "postgresql-%s" % pg_version
    elif os_family() == "Debian":
        if get_pg_type() == "PG":
            service = "postgresql@%s-main" % pg_version

    assert host.service(service).is_running, "Postgres service not running"

    assert host.service(service).is_enabled, "Postgres service not enabled"


def test_init_dbserver_socket():
    ansible_vars = load_ansible_vars()
    host = get_primary()
    
    if get_pg_type() == "PG":
        if ansible_vars.get("pg_port", 0):
            pg_port = ansible_vars["pg_port"]
        else:
            pg_port = "5432"
    
    sockets = []

    if get_pg_type() == "PG":
        if ansible_vars.get("pg_unix_socket_directories", 0):
            socket_dir_list = ansible_vars["pg_unix_socket_directories"]
            for socket_dir in socket_dir_list:
                sockets.append("tcp://%s" % pg_port)
                sockets.append("unix://%s/.s.PGSQL.%s" % (socket_dir, pg_port))
        else:
            socket_dir = get_pg_unix_socket_dir()
            sockets = [
                "tcp://%s" % pg_port, "unix://%s/.s.PGSQL.%s" % (socket_dir, pg_port)
            ]
        
    for socket in sockets:
        assert host.socket(socket).is_listening, (
            "Postgres is not listening on %s" % socket
        )


def test_init_dbserver_data_directory():
    ansible_vars = load_ansible_vars()
    pg_data = ansible_vars["pg_data"]
    pg_user = ansible_vars["pg_owner"]

    host = get_primary()

    if ansible_vars.get("pg_port", 0):
        pg_port = ansible_vars["pg_port"]
    else:
        pg_port = "5432"

    if ansible_vars.get("pg_unix_socket_directories", 0):
        socket_dir = ansible_vars["pg_unix_socket_directories"][0]
    else:
        socket_dir = get_pg_unix_socket_dir()

    with host.sudo(pg_user):
        query = "SELECT setting FROM pg_settings WHERE name = 'data_directory'"
        cmd = host.run(
            'psql -At -h %s -p %s -c "%s" postgres' % (socket_dir, pg_port, query)
        )

        data_directory = cmd.stdout.strip()
        assert host.file(data_directory).linked_to == pg_data, (
            "Postgres data_directory is not linked to '%s'" % pg_data
        )
