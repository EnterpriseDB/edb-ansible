#!env python3
# encoding: utf-8

import argparse
from multiprocessing import Pool
import os as os_
from pathlib import Path
import re
import sys
import subprocess
import yaml


class PgVersionChecker(argparse.Action):
    available_versions = ['10', '11', '12', '13', '14']

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_versions:
                parser.error("Postgres version %s not supported" % v)
        setattr(namespace, self.dest, values)


class PgTypeChecker(argparse.Action):
    available_types = ['EPAS', 'PG']

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_types:
                parser.error("Postgres type %s not supported" % v)
        setattr(namespace, self.dest, values)


class OSChecker(argparse.Action):
    available_os = ['centos7', 'rocky8', 'debian9', 'debian10', 'ubuntu20',
                    'oraclelinux7']

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_os:
                parser.error("Operating system %s not supported" % v)
        setattr(namespace, self.dest, values)


def load_configuration(configuration):
    return yaml.load(configuration.read(), Loader=yaml.Loader)


def exec_test_case(case_name, case_config, edb_repo_username,
                   edb_repo_password, pg_version_list, pg_type_list, os_list,
                   edb_enable_repo):
    n_success = 0
    n_executed = 0
    for os in case_config['os']:
        if len(os_list) > 0 and os not in os_list:
            continue
        for pg_type in case_config['pg_type']:
            if len(pg_type_list) > 0 and pg_type not in pg_type_list:
                continue
            for pg_version in case_config['pg_version']:
                pg_version = str(pg_version)
                if len(pg_version_list) > 0 and \
                        pg_version not in pg_version_list:
                    continue
                # Execute the test
                success = exec_test(
                    case_name,
                    edb_repo_username,
                    edb_repo_password,
                    os,
                    pg_type,
                    pg_version,
                    edb_enable_repo,
                )
                n_executed += 1
                if success:
                    n_success += 1
    return (n_success, n_executed)


def exec_test(case_name, edb_repo_username, edb_repo_password, os, pg_type,
              pg_version, edb_enable_repo):
    env = os_.environ.copy()
    env.update({
        'EDB_REPO_USERNAME': edb_repo_username,
        'EDB_REPO_PASSWORD': edb_repo_password,
        'EDB_ENABLE_REPO': edb_enable_repo,
        'EDB_PG_VERSION': pg_version,
        'EDB_PG_TYPE': pg_type,
    })

    # Tears down containers for this test case, just in case some containers
    # are still running here.
    tears_down(case_name)

    r = subprocess.run(
        'make -C cases/%s %s' % (case_name, os),
        shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env,
    )
    if r.returncode != 0:
        test_result = '\033[1m\033[91mFAILED\033[0m\n'
    else:
        test_result = '\033[1m\033[92mOK\033[0m\n'
    sys.stdout.write(
        "Test %s with %s/%s on %s ... %s"
        % (case_name, pg_type, pg_version, os, test_result)
    )
    sys.stdout.flush()

    if r.returncode != 0:
        log_stdout(case_name, os, pg_type, pg_version, r.stdout)
        log_stderr(case_name, os, pg_type, pg_version, r.stderr)

    # Tears down containers
    tears_down(case_name)

    return (r.returncode == 0)

def tears_down(case_name):
    r = subprocess.run(
        ['make', '-C', 'cases/%s' % case_name, 'clean'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if r.returncode != 0:
        raise Exception(r.stderr.decode('utf-8'))


def make_build():
    r = subprocess.run(
        ['make', '-C', '..', 'clean', 'build'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if r.returncode != 0:
        raise Exception(r.stderr.decode('utf-8'))


def make_log_dir():
    if not Path('./logs').exists():
        os_.mkdir('logs')


def log_stdout(case_name, os, pg_type, pg_version, stdout):
    log_name = 'logs/%s_%s_%s_%s.stdout' % (case_name, os, pg_type, pg_version)
    with open(log_name, 'wb') as f:
        f.write(stdout)


def log_stderr(case_name, os, pg_type, pg_version, stderr):
    log_name = 'logs/%s_%s_%s_%s.stderr' % (case_name, os, pg_type, pg_version)
    with open(log_name, 'wb') as f:
        f.write(stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-j', '--jobs',
        dest='jobs',
        type=int,
        help="Number of parallel jobs. Default: %(default)s",
        default=4,
    )
    parser.add_argument(
        '--configuration',
        dest='configuration',
        type=argparse.FileType('r', encoding='UTF-8'),
        help="Configuration file",
        default='config.yml',
    )

    parser.add_argument(
        '--edb-repo-username',
        dest='edb_repo_username',
        type=str,
        default='',
        help="EDB package repository username",
    )
    parser.add_argument(
        '--edb-repo-password',
        dest='edb_repo_password',
        type=str,
        default='',
        help="EDB package repository password",
    )
    parser.add_argument(
        '--edb-enable-repo',
        dest='edb_enable_repo',
        choices=['true', 'false'],
        default='true',
        help="Use EDB package repository",
    )
    parser.add_argument(
        '--pg-version',
        dest='pg_version',
        nargs='+',
        default=['14'],
        action=PgVersionChecker,
        help="Postgres versions list. Default: %(default)s",
    )
    parser.add_argument(
        '--pg-type',
        dest='pg_type',
        nargs='+',
        default=[],
        action=PgTypeChecker,
        help="Postgres DB engines list. Default: all",
    )
    parser.add_argument(
        '--os',
        dest='os',
        nargs='+',
        default=[],
        action=OSChecker,
        help="Operating systems list. Default: all",
    )
    parser.add_argument(
        '-k', '--keywords',
        dest='keyword',
        nargs='+',
        default=[],
        help="Execute test cases with a name matching the given keywords.",
    )
    env = parser.parse_args()

    make_build()
    make_log_dir()

    test_cases = []

    for name, config in load_configuration(env.configuration)['cases'].items():

        execute_test = False if len(env.keyword) > 0 else True

        for k in env.keyword:
            if re.search(re.escape(k), name):
                execute_test = True

        if not execute_test:
            continue

        test_cases.append(
            (name, config, env.edb_repo_username, env.edb_repo_password,
             env.pg_version, env.pg_type, env.os, env.edb_enable_repo)
        )


    with Pool(env.jobs) as p:
        r = p.starmap(exec_test_case, test_cases)
        p.close()
        p.join()
        if len(test_cases) > 0:
            n_executed = sum([x[1] for x in r])
            n_success = sum([x[0] for x in r])
            ratio = float(n_success) / float(n_executed) * 100
            print(
                "\nTests passed: %s/%s %.2f%%" % (n_success, n_executed, ratio)
            )
