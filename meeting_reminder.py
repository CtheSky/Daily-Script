import os
import shelve
import datetime
import subprocess

# Two types of remind message
# TODO add storage and add/update/delete interface for messages


this_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(this_dir, 'meeting_reminder')

db = shelve.open(db_path, writeback=True)


def say(words):
    subprocess.check_call('say %s' % words, shell=True)


def get_who_am_i_str():
    return '我是一个 cron job '


def get_time_str():
    """round time to nearest 10 min point and return """
    tm = datetime.datetime.now()
    tm += datetime.timedelta(minutes=5)
    tm -= datetime.timedelta(minutes=tm.minute % 10, seconds=tm.second, microseconds=tm.microsecond)

    return tm.strftime('%I:%M') + '到了 '


def get_remind_str():
    return '我们应该开会啦'


def prepare_words_to_say():
    return get_who_am_i_str() + get_time_str() + get_remind_str()


def main():
    words = prepare_words_to_say()
    say(words)


if __name__ == '__main__':
    main()
