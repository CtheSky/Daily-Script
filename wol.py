"""
Send magic packet for wol (wake-on-lane) to given mac address
See more here: https://en.wikipedia.org/wiki/Wake-on-LAN
>>> send_packet('5e:00:70:22:68:00')

Command line interface:
> python wol.py -h
usage: Send WOL magic packet to MAC [-h] mac

positional arguments:
  mac         MAC address to send magic packet

optional arguments:
  -h, --help  show this help message and exit
> python wol.py 5e:00:70:22:68:00
"""
import struct
import socket


def send_packet(mac_str):
    """Send magic packet to given mac address
    :param mac_str: mac address string separated by :
    :return:
    """
    def broadcast(magic):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(magic, ('<broadcast>', 9))

    def build_packet(mac_str):
        bytes = [255] * 6 + [int(x, 16) for x in mac_str.split(':')] * 16
        magic = struct.pack('B' * 102, *bytes)
        return magic

    magic_packet = build_packet(mac_str)
    broadcast(magic_packet)


def main():
    import argparse

    parser = argparse.ArgumentParser('Send WOL magic packet to MAC')
    parser.add_argument('mac', help='MAC address to send magic packet')

    args = parser.parse_args()
    mac = args.mac

    send_packet(mac)


if __name__ == '__main__':
    main()
