def main():
    import argparse
    import subprocess
    from fcntl import ioctl

    # handle command line args
    parser = argparse.ArgumentParser(
        'Reset USB device status. '
        'Use device name or a pair of bus and device number. '
        '"lsusb" command can be used to find those information.'
    )
    parser.add_argument('-b', '-bus', help='Bus number of USB port', default=0, dest='bus')
    parser.add_argument('-d', '-dev', help='Device number of USB port', default=0, dest='dev')
    parser.add_argument('-n', '-name', help='Device name', default=None, dest='name')

    args = parser.parse_args()
    bus, dev, name = int(args.bus), int(args.dev), args.name

    # find bus & device num of given name
    if args.name:
        cmd_output = subprocess.check_output(['lsusb'], universal_newlines=True)
        for line in cmd_output.splitlines():
            if args.name in line:
                _, bus, _, dev = line.split(':')[0].split()
                bus, dev = int(bus), int(dev)
                break

    # exit if no provided bus and device num
    if not bus or not dev:
        print('Please provide bus and device number, or a valid device name.')
        exit(1)

    # reset USB device status
    filename = "/dev/bus/usb/{:03d}/{:03d}".format(bus, dev)
    USBDEVFS_RESET = ord('U') << (4 * 2) | 20  # Equivalent of the _IO('U', 20) constant in the linux kernel.
    with open(filename, "wb") as fd:
        ioctl(fd, USBDEVFS_RESET, 0)


if __name__ == '__main__':
    main()
