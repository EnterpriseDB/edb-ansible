import pytest
import json

from conftest import (
    load_ansible_vars,
    get_hosts,
    get_os,
    get_pg_type,
    get_primary,
    get_standbys,
    get_pg_unix_socket_dir,
    get_pg_cluster_nodes
)

