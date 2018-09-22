import os
import sys
import paramiko


def establish_connected_client(host):
    """find connection info from ssh config file, connect the client and return"""
    client = paramiko.SSHClient()
    client._policy = paramiko.WarningPolicy()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # load content from ssh config file
    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    try:
        with open(user_config_file) as f:
            ssh_config.parse(f)
    except FileNotFoundError:
        print("{} file could not be found. Aborting.".format(user_config_file))
        sys.exit(1)

    # find config with matching hostname
    cfg = ssh_config.lookup(host)
    if not cfg:
        print("{} not found in ssh config file.".format(host))
        sys.exit(1)

    # connect the client
    client.connect(
        hostname=cfg['hostname'],
        username=cfg['user'],
        port=cfg.get('port', 22),
        key_filename=cfg.get('identityfile')
    )

    return client


def exec_command_and_print_stdout(client, command):
    print('Executing command: {}'.format(command).center(50, '='))

    _, stdout, stderr = client.exec_command(command)

    while not stdout.channel.exit_status_ready() or stdout.channel.recv_ready():
        output = stdout.channel.recv(1024)
        print(str(output, "utf8"))


def main():
    client = establish_connected_client('gcp')

    # install necessary packages
    commands = [
        'sudo apt-get update',
        'sudo apt-get install git',
        'sudo apt-get install python-pip',
        'sudo pip install git+https://github.com/shadowsocks/shadowsocks.git@master'
    ]

    for cmd in commands:
        exec_command_and_print_stdout(client, cmd)


if __name__ == '__main__':
    main()
