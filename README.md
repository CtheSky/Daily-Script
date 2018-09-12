# Daily-Script
Scripts that make my life easier.

### play_subtitle.py
Play `ass`, `webvtt` and `srt` format subtitle file in command line. Sometimes I want to watch video online but there's no suppport for loading 
subtitle file. Made a simple one so I don't have to download video. 
```shell
> python play_ass.py -h
usage: Display .ass format subtitle file. [-h] [-n N] [-t TIME] filename

positional arguments:
  filename              path to .ass file

optional arguments:
  -h, --help            show this help message and exit
  -n N                  N seconds to wait before display
  -t TIME, --time TIME  when to start, format is "hh:mm:ss"
```
### reset_usb.py
Reset the USB device given its name or bus&device number. My audio needs to be replugged to work properly, now I use
this script to reset it automatically when system boots.
```shell
> python reset_usb.py -h
usage: Reset USB device status. Use device name or a pair of bus and device number. "lsusb" command can be used to find those information.
       [-h] [-b BUS] [-d DEV] [-n NAME]

optional arguments:
  -h, --help           show this help message and exit
  -b BUS, -bus BUS     Bus number of USB port
  -d DEV, -dev DEV     Device number of USB port
  -n NAME, -name NAME  Device name
```

### wol.py
Send a [WOL](https://en.wikipedia.org/wiki/Wake-on-LAN)(Wake-on-LAN) packet to a given MAC address. Used to start my PC remotely.
```bash
> python wol.py -h
usage: Send WOL magic packet to MAC [-h] mac

positional arguments:
  mac         MAC address to send magic packet

optional arguments:
  -h, --help  show this help message and exit
> python wol.py 5e:00:70:22:68:00
```
### osx_notify.py
Emit OSX notification with custom title and content. Used together with cron to remind myself to leave chair and do some exercise.
```bash
> python osx_notify.py -h
usage: Emit OSX notification with custom title and content.

positional arguments:
  title       Title of the notification
  content     Content of the notification

optional arguments:
  -h, --help  show this help message and exit
> python osx_notify.py title content
```
