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
    print('Start executing command'.center(50, '='))
    print(command)
    print('Command Output'.center(50, '='))

    _, stdout, stderr = client.exec_command(command)

    while not stdout.channel.exit_status_ready() or stdout.channel.recv_ready():
        output = stdout.channel.recv(1024)
        print(str(output, "utf8"))


def install_packages(client):
    """install necessary packages"""
    commands = [
        'sudo apt-get -y update',
        'sudo apt-get -y install git',
        'sudo apt-get -y install python-pip',
        'sudo pip install git+https://github.com/shadowsocks/shadowsocks.git@master'
    ]

    for cmd in commands:
        exec_command_and_print_stdout(client, cmd)


def config_and_setup_server(client):
    cmd_tpl = 'sudo ssserver -s {server_address} -p {server_port} -k {password} -m {method} -d start'

    class Option:
        def __init__(self, name, default):
            self.name = name
            self.default = default
            self.value = None

    options = [
        Option(name='server_address', default='127.0.0.1'),
        Option(name='server_port', default='2333'),
        Option(name='password', default='123456'),
        Option(name='method', default='aes-256-cfb')
    ]

    while True:
        print('Please specify the config option for the server:')
        for option in options:
            option.value = input('Option name : [{}], Default value: [{}]\n'.format(option.name, option.default))

        kwargs = {option.name: option.default if not option.value else option.value for option in options}
        cmd = cmd_tpl.format(**kwargs)

        y_or_n = input('Is [{}] correct? [Y/n]'.format(cmd))
        if not y_or_n or y_or_n.lower() in ['y', 'yes']:
            client.exec_command(cmd)
            sys.exit(0)


def main():
    import argparse

    parser = argparse.ArgumentParser('Read ssh config, connect to the remote, '
                                     'install packages and setup shadowsocks server. (Only work for debian now)')
    parser.add_argument('--host', help='host configured in .ssh/config file')

    args = parser.parse_args()
    host = args.host

    client = establish_connected_client(host)
    install_packages(client)
    config_and_setup_server(client)


if __name__ == '__main__':
    main()
