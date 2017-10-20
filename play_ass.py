def get_events(filename):
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


def display_events(events):
    import time

    def to_seconds(timestr):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, map(float, timestr.split(':')))])

    begin_time = time.time()
    for start, end, text in events:

        while time.time() < begin_time + to_seconds(start):
            time.sleep(0.01)
        print(text)

        while time.time() < begin_time + to_seconds(end):
            time.sleep(0.01)
        print()


if __name__ == '__main__':
    events = get_events('sc.ass')
    display_events(events)
