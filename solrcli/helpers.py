import paramiko
from paramiko import SSHClient
from scp import SCPClient


def get_from_scp(cfg, filename, localpath):
    host = cfg.get('host')
    user = cfg.get('user')
    key = cfg.get('key', None)

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if key:
        private_key = paramiko.RSAKey.from_private_key_file(key)
        ssh.connect(host, username=user, pkey=private_key)
    else:
        ssh.load_system_host_keys()
        ssh.connect(host)

    scp = SCPClient(ssh.get_transport())

    scp.get(filename, local_path=localpath)
