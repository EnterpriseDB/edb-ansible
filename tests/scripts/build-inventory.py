# coding: utf-8

import argparse
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from lib import docker

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--compose-dir',
        dest='compose_dir',
        type=Path,
        help="Docker Compose directory. Default: %(default)s",
        default='.',
    )
    env = parser.parse_args()

    docker_inventory = docker.DockerInventory(cwd=env.compose_dir)
    docker_inventory.discover()

    inventory_vars = {}
    for c in docker_inventory.containers:
        (inventory_name, os) = c['Service'].split('-')
        container = docker.DockerOSContainer(c['ID'], os)
        inventory_vars["%s_ip" % inventory_name] = container.ip()

    templates_dir = env.compose_dir
    file_loader = FileSystemLoader(templates_dir)
    jenv = Environment(loader=file_loader, trim_blocks=True)
    template = jenv.get_template('inventory.yml.j2')

    with open(env.compose_dir / 'inventory.yml', 'w') as f:
        f.write(template.render(inventory_vars=inventory_vars))
