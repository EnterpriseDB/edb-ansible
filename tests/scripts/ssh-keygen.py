# coding: utf-8

import argparse
import os
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from lib import SSH_PRIVATE_KEY_FILE, SSH_PUBLIC_KEY_FILE

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ssh-dir",
        dest="ssh_dir",
        type=Path,
        help="SSH keys directory. Default: %(default)s",
        default=".ssh",
    )
    env = parser.parse_args()

    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=65537, key_size=2048
    )

    b_private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption(),
    )

    b_public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
    )

    if not env.ssh_dir.exists():
        os.makedirs(env.ssh_dir)

    with open(env.ssh_dir / SSH_PRIVATE_KEY_FILE, "wb") as f:
        f.write(b_private_key)

    with open(env.ssh_dir / SSH_PUBLIC_KEY_FILE, "wb") as f:
        f.write(b_public_key + b"\n")
