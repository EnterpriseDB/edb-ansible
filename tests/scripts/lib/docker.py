import json
import re
import shlex
import subprocess
import sys


class DockerInventory():
    def __init__(self, cwd='.'):
        self.cwd = cwd
        self.containers = []

    def discover(self):
        cp = subprocess.run(
            ['docker', 'compose', 'ps', '--format', 'json'],
            capture_output=True,
            cwd=self.cwd,
        )

        if cp.returncode != 0:
            raise Exception(cp.stderr.decode('utf-8'))

        b_output = cp.stdout
        if len(b_output) > 0:
            self.containers = json.loads(b_output)


class DockerContainer():
    def __init__(self, id):
        self.id = id

    def log(self, msg):
        sys.stdout.write("[%s] %s\r\n" % (self.id[0:8], msg))
        sys.stdout.flush()

    def exec(self, command):
        self.log("Executing %s" % command)
        a_command = shlex.split(command)
        cp = subprocess.run(
            ['docker', 'exec', self.id] + a_command,
            capture_output=True,
        )
        if cp.returncode != 0:
            raise Exception(cp.stderr.decode('utf-8'))
        return cp.stdout

    def send_file(self, local, dest):
        self.log("Copying local file %s to remote %s" % (local, dest))
        cp = subprocess.run(
            ['docker', 'cp', local, '%s:%s' % (self.id, dest)],
            capture_output=True,
        )
        if cp.returncode != 0:
            raise Exception(cp.stderr.decode('utf-8'))

    def ip(self):
        b_output = self.exec('/sbin/ip addr show eth0')
        output = b_output.decode('utf-8')

        m = re.search(r'inet ([0-9\.]+)', output)
        if m:
            return m.group(1)

    def mkdir(self, dir, mode='0700'):
        self.exec('/bin/mkdir -p %s' % dir)
        self.exec('/bin/chmod %s %s' % (mode, dir))

    def rm(self, path):
        self.exec('/bin/rm -rf %s' % path)

    def add_ssh_pub_key(self, ssh_pub_key_path):
        self.send_file(ssh_pub_key_path, '/root/.ssh/authorized_keys')
        self.exec('/bin/chmod 0600 /root/.ssh/authorized_keys')
        self.exec('/bin/chown root:root /root/.ssh/authorized_keys')

"""
CentOS/RockyLinux family
"""
class DockerCentosContainer(DockerContainer):

    def start_sshd(self):
        self.exec('/bin/systemctl start sshd')


class DockerCentos7Container(DockerCentosContainer):
    pass


class DockerRocky8Container(DockerCentosContainer):
    pass


class DockerOraclelinux7Container(DockerCentosContainer):
    pass


"""
Debian family
"""
class DockerDebianContainer(DockerContainer):

    def start_sshd(self):
        self.exec('/bin/systemctl start ssh.service')


class DockerDebian9Container(DockerDebianContainer):
    pass


class DockerDebian10Container(DockerDebianContainer):
    pass


class DockerUbuntu20Container(DockerDebianContainer):
    pass


def DockerOSContainer(id, os):
    if os == 'centos7':
        return DockerCentos7Container(id)
    elif os == 'rocky8':
        return DockerRocky8Container(id)
    elif os == 'debian9':
        return DockerDebian9Container(id)
    elif os == 'debian10':
        return DockerDebian10Container(id)
    elif os == 'ubuntu20':
        return DockerUbuntu20Container(id)
    elif os == 'oraclelinux7':
        return DockerOraclelinux7Container(id)
    else:
        raise Exception("Unknown OS %s" % os)
