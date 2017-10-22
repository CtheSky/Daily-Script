# Daily-Script
Scripts written to make my life easier.

### play_ass.py
Play `.ass` format subtitle file in command line. Sometimes I want to watch video online but there's no suppport for loading 
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
