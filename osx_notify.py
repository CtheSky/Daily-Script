"""
Emit OSX notification with custom title and content.
>>> notify('A Title', 'Content')

Command line interface:
> python osx_notify.py -h
usage: Emit OSX notification with custom title and content.

positional arguments:
  title       Title of the notification
  content     Content of the notification

optional arguments:
  -h, --help  show this help message and exit
> python osx_notify.py title content
"""
import os


def notify(title, content):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(content, title))


def main():
    import argparse

    parser = argparse.ArgumentParser('Send WOL magic packet to MAC')
    parser.add_argument('title', help='Title of the notification')
    parser.add_argument('content', help='Content of the notification')

    args = parser.parse_args()
    notify(title=args.title, content=args.content)


if __name__ == '__main__':
    main()
