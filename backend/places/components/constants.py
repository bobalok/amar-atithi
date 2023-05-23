def checkin_times():
    times = [
        {'value': 0, 'text': "Flexible"},
        {'value': 10, 'text': "9AM"},
        {'value': 11, 'text': "10AM"},
        {'value': 12, 'text': "11AM"},
        {'value': 13, 'text': "12PM (Noon)"},
        {'value': 14, 'text': "1PM"},
        {'value': 15, 'text': "2PM"},
        {'value': 16, 'text': "3PM"},
        {'value': 17, 'text': "4PM"},
        {'value': 18, 'text': "5PM"},
        {'value': 19, 'text': "6PM"},
        {'value': 20, 'text': "7PM"},
        {'value': 21, 'text': "8PM"},
        {'value': 22, 'text': "9PM"},
        {'value': 23, 'text': "10PM"},
        {'value': 24, 'text': "11PM"},
        {'value': 1, 'text': "12AM (Midnight)"},
        {'value': 2, 'text': "1AM (Next Day)"},
        {'value': 3, 'text': "2AM (Next Day)"},
        {'value': 4, 'text': "3AM (Next Day)"},
        {'value': 5, 'text': "4AM (Next Day)"},
        {'value': 6, 'text': "5AM (Next Day)"},
        {'value': 7, 'text': "6AM (Next Day)"},
        {'value': 8, 'text': "7AM (Next Day)"},
        {'value': 9, 'text': "8AM (Next Day)"},
    ]

    return times

def to_checkin_time(time):
    for t in checkin_times():
        if t.get("value") == time:
            return t.get("text")

    return ""

def checkout_times():
    times = [
        {'value': 1, 'text': "12AM (Midnight)"},
        {'value': 2, 'text': "1AM"},
        {'value': 3, 'text': "2AM"},
        {'value': 4, 'text': "3AM"},
        {'value': 5, 'text': "4AM"},
        {'value': 6, 'text': "5AM"},
        {'value': 7, 'text': "6AM"},
        {'value': 8, 'text': "7AM"},
        {'value': 9, 'text': "8AM"},
        {'value': 10, 'text': "9AM"},
        {'value': 11, 'text': "10AM"},
        {'value': 12, 'text': "11AM"},
        {'value': 13, 'text': "12PM (Noon)"},
        {'value': 14, 'text': "1PM"},
        {'value': 15, 'text': "2PM"},
        {'value': 16, 'text': "3PM"},
        {'value': 17, 'text': "4PM"},
        {'value': 18, 'text': "5PM"},
        {'value': 19, 'text': "6PM"},
        {'value': 20, 'text': "7PM"},
        {'value': 21, 'text': "8PM"},
        {'value': 22, 'text': "9PM"},
        {'value': 23, 'text': "10PM"},
        {'value': 24, 'text': "11PM"},
    ]

    return times


def to_checkout_time(time):
    for t in checkout_times():
        if t.get("value") == time:
            return t.get("text")

    return ""