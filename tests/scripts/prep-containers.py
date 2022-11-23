# coding: utf-8

import argparse
from multiprocessing import Pool
from pathlib import Path

from lib import SSH_PUBLIC_KEY_FILE, docker


def prep_container(id, os, ssh_dir):
    c = docker.DockerOSContainer(id, os)

    # Common commands
    c.rm("/root/.ssh")
    c.mkdir("/root/.ssh", mode="0700")

    c.start_sshd()
    c.add_ssh_pub_key(ssh_dir / SSH_PUBLIC_KEY_FILE)


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

    args = [
        (c["ID"], c["Service"].split("-")[1], env.ssh_dir)
        for c in docker_inventory.containers
    ]

    with Pool(len(args)) as p:
        p.starmap(prep_container, args)
        p.close()
        p.join()
