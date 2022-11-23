from conftest import get_pgbackrestserver, load_ansible_vars


def test_setup_pgbackrestserver_packages():
    host = get_pgbackrestserver()
    packages = ["pgbackrest"]

    for package in packages:
        assert host.package(package).is_installed, "Package %s not installed" % packages


def test_setup_pgbackrestserver_config_file():
    host = get_pgbackrestserver()
    ansible_vars = load_ansible_vars()
    config_file = ansible_vars["pgbackrest_configuration_file"]

    assert host.file(config_file).exists, "%s does not exist" % config_file


def test_setup_pgbackrestserver_configuration():
    host = get_pgbackrestserver()
    ansible_vars = load_ansible_vars()
    pgbackrest_user = ansible_vars["pgbackrest_user"]

    with host.sudo(pgbackrest_user):
        cmd = host.run("pgbackrest --stanza=main check")
        result = cmd.stdout.strip()

    assert (
        "completed successfully" in result
    ), "Configuration for pgBackRest is not properly done."
