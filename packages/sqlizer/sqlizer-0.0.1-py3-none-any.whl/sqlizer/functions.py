from datetime import timedelta, datetime


def today(format='%YY-%m-%d'):
    return datetime.today().strftime(format)


def yesterday(format='%Y-%m-%d'):
    dt = datetime.today() - timedelta(days=1)
    return dt.strftime(format)


def days_ago(number_of_days: int, format='%Y-%m-%d'):
    dt = datetime.today() - timedelta(days=int(number_of_days))
    return dt.strftime(format)
