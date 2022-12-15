import pytest
from conftest import get_pg_type, get_pg_version, get_primary, load_ansible_vars


def test_install_extension_pg():
    if get_pg_type() != "PG":
        pytest.skip()

    packages = []
    required_packages = []

    host = get_primary()
    pg_version = get_pg_version()
    ansible_vars = load_ansible_vars()
    extensions = ansible_vars["supported_extension"]

    for extension in extensions:
        packages += [
            "%s" % extension["extension_package"]
        ]
        if "required_package" in extension:
            required_packages += extension["required_package"]

    for package in packages:
        assert host.package(package).is_installed, "Extension Package %s not installed" % packages
    for package in required_packages:
        assert host.package(package).is_installed, "Required Package %s not installed" % package
