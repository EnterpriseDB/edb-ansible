import pytest

from conftest import (
    load_ansible_vars,
    get_pg_type,
    get_pg_version,
    get_primary,
    os_family
)


def test_touchstone_appimage():
    host = get_primary()
    appimage_bin_location = "/usr/bin/ts"

    assert host.file(appimage_bin_location).exists, \
        "touchstone appimage not installed correctly."


def test_touchstone_packages():
    host = get_primary()
    packages = [
        'fuse',
        'perf',
        'sysstat',
        'util-linux'
    ]

    if os_family() == 'RedHat':
        packages.append('fuse-libs')

    for package in packages:
        assert host.package(package).is_installed, \
            "Package %s not installed" % package
