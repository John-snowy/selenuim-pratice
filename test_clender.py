import calendar
import datetime

if __name__ == '__main__':

    today = datetime.datetime.today()
    year = today.year
    month = today.month
    end = calendar.monthrange(year, month)[1]
    start_weekday = calendar.weekday(year, month, 1)
    end_weekday = calendar.weekday(year, month, end)
    print(start_weekday)
    print(end_weekday)