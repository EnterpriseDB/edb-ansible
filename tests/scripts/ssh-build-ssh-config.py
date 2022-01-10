# coding: utf-8

import argparse
from os import chmod
from pathlib import Path


def build_ssh_config(ssh_dir, name='ssh_config'):
    ssh_config = """
Host *
    StrictHostKeyChecking no
    """
    with open(ssh_dir / name, 'w') as f:
        f.write(ssh_config)
    chmod(ssh_dir / name, 0o600)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ssh-dir',
        dest='ssh_dir',
        type=Path,
        help="SSH keys directory. Default: %(default)s",
        default='.ssh',
    )
    env = parser.parse_args()

    build_ssh_config(env.ssh_dir)
