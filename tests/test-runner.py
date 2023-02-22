#!env python3
# encoding: utf-8

import argparse
import itertools
import os
import re
import shlex
import subprocess
from multiprocessing import Pool
from pathlib import Path

import termcolor
import yaml


class ColoredPrinter:
    colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]

    def print_message(self, message):
        pid = os.getpid()
        color = self.colors[pid % len(self.colors)]
        text = termcolor.colored(f"[PID={pid}] " + message, color)
        print(text)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TestConfiguration(metaclass=Singleton):
    def __init__(self):
        config_path = "test-config.yml"
        with open(config_path, "r") as config_file:
            self.config = yaml.load(config_file, Loader=yaml.BaseLoader)

    def __getitem__(self, item):
        return self.config[item]


class PgVersionChecker(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        config = TestConfiguration()
        self.available_versions = config["available_pg_versions"]
        super(PgVersionChecker, self).__init__(option_strings, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_versions:
                parser.error("Postgres version %s not supported" % v)
        setattr(namespace, self.dest, values)


class PgTypeChecker(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        config = TestConfiguration()
        self.available_types = config["available_pg_types"]
        super(PgTypeChecker, self).__init__(option_strings, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_types:
                parser.error("Postgres type %s not supported" % v)
        setattr(namespace, self.dest, values)


class OSChecker(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        config = TestConfiguration()
        self.available_os_types = config["available_os_types"]
        super(OSChecker, self).__init__(option_strings, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        for v in values:
            if v not in self.available_os_types:
                parser.error("Operating system %s not supported" % v)
        setattr(namespace, self.dest, values)


def main():
    args = get_input_arguments()

    if args.remove_containers:
        invoke_make_clean_for_all_directories()
        quit()

    testing_roles = get_testing_roles_from_keywords(args.keyword)
    make_ansible_collection_tar_ball()
    make_log_dir()

    if not testing_roles:
        print("No test cases matching with the given keywords")
        quit()

    args_for_exec_test = get_args_for_exec_test(testing_roles, args)

    with Pool(args.jobs) as p:
        results = p.starmap(exec_test, args_for_exec_test)
        print_test_result(results)


def invoke_make_clean_for_all_directories():
    r = subprocess.run(["make", "-f", "Makefile.mk", "clean_all"])
    if r.returncode != 0:
        raise Exception(r.stderr.decode("utf-8"))


def make_ansible_collection_tar_ball():
    r = subprocess.run(
        ["make", "-C", "..", "clean_for_test", "build_for_test"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if r.returncode != 0:
        raise Exception(r.stderr.decode("utf-8"))


def make_log_dir():
    if not Path("./logs").exists():
        os.mkdir("logs")


def get_input_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j",
        "--jobs",
        dest="jobs",
        type=int,
        help="Number of parallel jobs. Default: %(default)s",
        default=4,
    )

    parser.add_argument(
        "--pg-type",
        dest="pg_type",
        nargs="+",
        default=["PG"],
        action=PgTypeChecker,
        help="Postgres DB engines list. Default: %(default)s",
    )

    parser.add_argument(
        "--pg-version",
        dest="pg_version",
        nargs="+",
        default=["14.6"],
        action=PgVersionChecker,
        help="Postgres versions list. Default: %(default)s",
    )

    parser.add_argument(
        "--os-type",
        dest="os_type",
        nargs="+",
        default=["centos7"],
        action=OSChecker,
        help="Operating systems list. Default: %(default)s",
    )

    parser.add_argument(
        "-k",
        "--keywords",
        dest="keyword",
        nargs="+",
        default=[""],
        help="Execute test cases with a name matching the given keywords.",
    )

    parser.add_argument(
        "-m",
        "--maintain-containers",
        dest="maintain_containers",
        action="store_true",
        help=".",
    )

    parser.add_argument(
        "-r",
        "--remove-containers",
        dest="remove_containers",
        action="store_true",
        help="Remove all containers created from this test.",
    )

    return parser.parse_args()


def get_testing_roles_from_keywords(keywords):
    testing_roles = []
    for keyword in keywords:
        for role in TestConfiguration()["available_roles"]:
            if re.search(re.escape(keyword), role):
                testing_roles.append(role)

    return testing_roles


def get_args_for_exec_test(testing_roles, args):
    return [(role, args) for role in testing_roles]


def exec_test(case_name, args):
    executed = 0
    success = 0
    pg_types = args.pg_type
    pg_versions = args.pg_version
    os_types = args.os_type
    maintain_containers = args.maintain_containers
    for iter in itertools.product([case_name], pg_types, pg_versions, os_types):
        if exec_test_case(*iter):
            success = success + 1
        executed = executed + 1
        if not maintain_containers:
            tears_down(case_name)

    return (executed, success)


def exec_test_case(case_name, pg_type, pg_version, os_type):
    env = os.environ.copy()
    env.update(
        {
            "OPENSQL_PG_VERSION": pg_version,
            "OPENSQL_PG_TYPE": pg_type,
            "OPENSQL_OS_TYPE": os_type,
            "CASE_NAME": case_name,
        }
    )

    result = use_makefile_to_run(case_name, pg_type, pg_version, os_type, env)

    return result


def tears_down(case_name):
    r = subprocess.run(
        ["make", "-C", "cases/%s" % case_name, "clean"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if r.returncode != 0:
        raise Exception(r.stderr.decode("utf-8"))


def use_makefile_to_run(case_name, pg_type, pg_version, os_type, env):
    printer = ColoredPrinter()
    message = f"Testing...(case={case_name}, pg_type={pg_type}, pg_version={pg_version}, os_type={os_type})"
    printer.print_message(message)

    command = shlex.split(f"make -C cases/{case_name} {os_type}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        close_fds=True,
        env=env,
    )

    stdout_logfile_name = f"logs/{case_name}_{os_type}_{pg_type}_{pg_version}.stdout"
    stdout_logfile = open(stdout_logfile_name, "wb", buffering=0)
    printer.print_message(f"Logs are written in {stdout_logfile_name}")

    while process.poll() is None:
        line = process.stdout.readline()
        stdout_logfile.write(line)

    stdout_logfile.close()
    exitcode = process.wait()

    result_message = "Success" if exitcode == 0 else "Fail"
    printer.print_message(
        f"Test Complete...({case_name}, {pg_type}, {pg_version}, {os_type}) with result: {result_message}"
    )

    return exitcode == 0


def print_test_result(results):
    n_executed = sum([x[0] for x in results])
    n_success = sum([x[1] for x in results])
    ratio = float(n_success) / float(n_executed) * 100
    print("\nTests passed: %s/%s %.2f%%" % (n_success, n_executed, ratio))


if __name__ == "__main__":
    main()
