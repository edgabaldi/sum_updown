#!/usr/bin/env python
import datetime
import math

def decimal_to_time(decimal_time):
    """
    >>> decimal_to_time(1.0)
    datetime.time(1, 0)
    >>> decimal_to_time(23.450)
    datetime.time(23, 27)
    """
    hours = int(decimal_time)
    minutes = (decimal_time * 60) % 60
    seconds = (decimal_time * 3600) % 60

    args = [int(n) for n in [hours, minutes, seconds]]

    return datetime.time(*args)


def _wrap_decimal_to_hour(decimal_hour, level = 0):
    aux = math.modf(decimal_hour)
    level+=1
    if level == 3:
        return int(aux[1])
    else:
        return str(int(aux[1])) + ':' + str(_wrap_decimal_to_hour(aux[0]*60, level))

def decimal_to_hour(decimal_hour, level = 0):
    """
    >>> decimal_to_hour(1.0)
    datetime.time(1, 0)
    >>> decimal_to_hour(23.450)
    datetime.time(23, 26, 59)
    """
    time_str = _wrap_decimal_to_hour(decimal_hour)
    return datetime.time(*[int(n) for n in time_str.split(':')])


class SumUpDown(object):
    """
    >>> time = SumUpDown(datetime.date(2013, 4, 15), -14.408749, 52.1421448)
    >>> time.calculate()
    {'start': datetime.time(6, 38, 20), 'end': datetime.time(18, 18, 48)}
    """

    def __init__(self, date, latitude, longitude):
        self.date = date
        self.latitude = latitude
        self.longitude = longitude

    def get_timezone(self):
        return math.trunc(self.longitude/15)

    def get_fixed_longitude(self):
        value = self.longitude - (self.get_timezone() * 15)
        return value * 60 / 15 / 60

    def get_day_of_year(self):
        datetuple = self.date.timetuple()
        return datetuple[7]

    def get_decline_of_earth(self):
        return 23.45 * math.sin(math.radians(360.0/365.0 * (284 + self.get_day_of_year())))

    def get_sunshine_hours(self):
        x = math.tan(math.radians(self.get_decline_of_earth()))
        y = math.tan(math.radians(self.latitude))
        return 2.0/15.0 * math.degrees(math.acos(-x*y))

    def calculate(self):
        value = self.get_sunshine_hours() / 2
        sunrise = 12 - value + self.get_fixed_longitude()
        sunset = 12 + value + self.get_fixed_longitude()
        return {
            'start': decimal_to_hour(sunrise),
            'end': decimal_to_hour(sunset),
        }
