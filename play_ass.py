def get_events(filename):
    """parse .ass file, return a list of (start, end, text)"""
    with open(filename) as f:
        ass = f.read()

        events_str = ass.split('[Events]\n', maxsplit=1)[1]
        format_line, *event_lines = events_str.splitlines()

        from operator import itemgetter
        columns = [c.strip().lower() for c in format_line.split('Format:')[1].split(',')]
        get_layer = itemgetter(columns.index('layer'))
        get_start = itemgetter(columns.index('start'))
        get_end = itemgetter(columns.index('end'))
        get_effect = itemgetter(columns.index('effect'))
        get_text = itemgetter(columns.index('text'))

        def extract(line: str):
            values = line.split('Dialogue:')[1].split(',', maxsplit=len(columns))
            values = [v.strip() for v in values]
            return get_layer(values), get_start(values), get_end(values), get_effect(values), get_text(values)

        events = []
        dialog_lines = [line for line in event_lines if line.startswith('Dialogue:')]
        for line in dialog_lines:
            layer, start, end, effect, text = extract(line)
            if layer == '0' and not effect:
                events.append((start, end, text))

        return events


def display_events(events, shift):
    """display the text according to its start and end time, time starts at 'shift'"""
    import sys
    write, flush = sys.stdout.write, sys.stdout.flush

    import time
    begin_time = time.time()
    msg, back_len = '', 0

    def update_msg(text):
        nonlocal msg
        seconds = time.time() - begin_time
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        time_str = "%d:%02d:%02d" % (h, m, s)
        msg = ' '.join([time_str, text])

    def flush_msg():
        nonlocal back_len
        write('\x08' * back_len + ' ' * back_len)
        write('\x08' * back_len + msg)
        flush()
        back_len = len(msg.encode('utf-8'))

    def to_seconds(time_str):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, map(float, time_str.split(':')))])

    if shift:
        begin_time -= to_seconds(shift)

    i = 0
    while i < len(events):
        start, end, text = events[i]
        if time.time() < begin_time + to_seconds(start):
            update_msg('')
        elif time.time() < begin_time + to_seconds(end):
            update_msg(text)
        else:
            i += 1

        flush_msg()
        time.sleep(0.01)


def n_seconds_to_prepare(n):
    """provide a n seconds delay for manually syncing the video"""
    import time
    for i in range(n, 0, -1):
        msg = '%d seconds to start.' % i
        print(msg, end='', flush=True)
        time.sleep(1)
        print('\r' + ' ' * len(msg) + '\r', end='', flush=True)


def main():
    import argparse

    parser = argparse.ArgumentParser('Display .ass format subtitle file.')
    parser.add_argument('filename', help='path to .ass file')
    parser.add_argument('-n', default=5, help='N seconds to wait before display')
    parser.add_argument('-t', '--time', default='', help='when to start, format is "hh:mm:ss"')

    args = parser.parse_args()
    filename = args.filename
    n = int(args.n)
    t = args.time

    events = get_events(filename=filename)
    n_seconds_to_prepare(n)
    display_events(events, shift=t)


if __name__ == '__main__':
    main()
