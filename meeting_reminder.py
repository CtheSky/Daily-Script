import os
import sys
import random
import shelve
import datetime
import subprocess


this_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(this_dir, 'meeting_reminder')

remind2index = shelve.open(db_path, writeback=True)


def say_remind():
    words = get_who_am_i_str() + get_time_str() + get_remind_str()
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
    if not remind2index:
        print('Please add a remind first')
        sys.exit()

    return random.choice(list(remind2index.keys()))


def list_remind_str():
    print('All reminds and their indices:')
    for remind, index in remind2index.items():
        print('%s : %s' % (index, remind))


def add_remind_str(remind_str):
    if remind_str in remind2index.keys():
        print('Already exists: %s' % remind_str)
    else:
        indices = remind2index.values()
        if not indices:
            index = 1
        else:
            indices_set = set(indices)
            full_set = set(range(1, max(indices)))

            unfilled_set = full_set - indices_set
            if unfilled_set:
                index = unfilled_set.pop()
            else:
                index = max(indices) + 1

        remind2index[remind_str] = index
        print('Added record [%s : %s]' % (index, remind_str))


def delete_remind_str(index):
    if index in remind2index.values():
        remind_str = [k for k, v in remind2index.items() if v == index][0]
        del remind2index[remind_str]
        print('Deleted record [%s: %s]' % (index, remind_str))
    else:
        print('Record with index [%s] not found' % index)


def main():
    import argparse

    parser = argparse.ArgumentParser('Emit OSX say command to report time and remind things.'
                                     'Only one option can be used each time.')
    parser.add_argument('--add', dest='remind', help='Add a remind string.')
    parser.add_argument('--list', action='store_true', help='List remind strings and indices.')
    parser.add_argument('--delete', dest='index_to_delete', type=int, help='Delete a remind string by index.')
    parser.add_argument('--say', dest='index_to_say', action='store_true',
                        help='Say a remind string. If no index provided, say a random one.')

    args = parser.parse_args()
    args_list = [args.remind, args.list, args.index_to_delete, args.index_to_say]
    used_args = [arg for arg in args_list if arg]
    if not used_args or len(used_args) > 1:
        print('One option should be specified. See [-h] option for more details.')
        return

    if args.list:
        list_remind_str()

    if args.remind:
        add_remind_str(args.remind)

    if args.index_to_delete:
        delete_remind_str(args.index_to_delete)

    if args.index_to_say:
        say_remind()


if __name__ == '__main__':
    main()
