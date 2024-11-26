import datetime


def check_data(day):
    dt_now = datetime.datetime.now()
    try:
        dt_dl = datetime.datetime.strptime(day, "%d.%m.%y %H:%M")
    except ValueError:
        return False
    return dt_dl > dt_now
