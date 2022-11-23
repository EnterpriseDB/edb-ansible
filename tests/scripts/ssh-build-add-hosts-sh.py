# coding: utf-8

import argparse
from os import chmod
from pathlib import Path

from lib import docker


def build_ssh_keyscan_script(containers, ssh_dir, name="add_hosts.sh"):
    with open(ssh_dir / name, "w") as f:
        f.write("#!/bin/bash\n")
        for container in containers:
            os = container["Service"].split("-")[1]
            c = docker.DockerOSContainer(container["ID"], os)
            ip = c.ip()
            f.write("ssh-keyscan -H %s >> ~/.ssh/known_hosts\n" % ip)

    chmod(ssh_dir / name, 0o755)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--compose-dir",
        dest="compose_dir",
        type=Path,
        help="Docker Compose directory. Default: %(default)s",
        default=".",
    )
    parser.add_argument(
        "--ssh-dir",
        dest="ssh_dir",
        type=Path,
        help="SSH keys directory. Default: %(default)s",
        default=".ssh",
    )
    env = parser.parse_args()

    docker_inventory = docker.DockerInventory(cwd=env.compose_dir)
    docker_inventory.discover()

    build_ssh_keyscan_script(docker_inventory.containers, env.ssh_dir)
