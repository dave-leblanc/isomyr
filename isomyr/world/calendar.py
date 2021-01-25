from datetime import datetime
from math import ceil

from isomyr.event import notify, subscribe
from isomyr.util.numbers import getOrdinal

# Real-time constants.
realSecond = 1
realMinute = realSecond * 60 
realHour = realMinute * 60
realDay = realHour * 24
realWeek = realDay * 7
realMonth = realWeek * 4
realYear = realDay * 365
realSeason = realYear / 4


# With this time setting, games will progress at a rate where an entire year
# passes after 5 minutes of real-time play.
SPEED_10 = realYear / (5 * realMinute)
# With this time setting, games will progress at a rate where an entire year
# passes after one hour of real-time play.
SPEED_09 = realYear / realHour
# With this time setting, games will progress at a rate where a quarter of a
# year (i.e., "season") passes after one hour of real-time play.
SPEED_08 = realSeason / realHour
# With this time setting, games will progress at a rate where a day passes
# after a minute of real-time play.
SPEED_07 = realDay / realMinute
# With this time setting, games will progress at a rate where a month passes
# after one hour of real-time play.
SPEED_06 = realMonth / realHour
# With this time setting, games will progress at a rate where a night passes in
# about 30 seconds.
SPEED_05 = (realDay / 8) / (realMinute / 2)
# With this time setting, games will progress at a rate where a week passes
# after one hour of real-time play.
SPEED_04 = realWeek / realHour
# With this time setting, games will progress at a rate where three days pass
# after one hour of real-time play.
SPEED_03 = (realDay * 3) / realHour
# With this time setting, games will progress at a rate where a half-hour
# passes after one minute of real-time play.
SPEED_02 = (realHour / 2) / realMinute
# With this time setting, games will progress at a rate where an hour passes
# after 5 minutes of real-time play (which is the same thing as a day passing
# after 30 miutes of real-time play).
SPEED_01 = realHour / (5 * realMinute)
# This speed setting indicates a 1-to-1 mapping from game time to real time. In
# other words, the in-game world time moves at the same rate as the real-life,
# out-of-game time.
SPEED_00 = 1


class TimeScale(object):
    """
    Time scale constants.
    """
    second = "secondScale"
    minute = "minuteScale"
    hour = "hourScale"
    day = "dayScale"
    month = "monthScale"
    year = "yearScale"


class TimeChange(object):
    """
    Time change constants.
    """
    hour = "hourChange"
    dawn = "toDawnChange"
    dusk = "toDuskChange"
    day = "dayChange"
    month = "monthChange"
    season = "seasonChange"
    year = "yearChange"


class Time(object):
    """
    This class is used to track world time as experienced by player characters
    in-game. It allows for the possibility of different worlds to have
    different time representations. For convenience, it uses the same units as
    Earth time for seconds, minutes, and hours.

    For games that don't need to track time on the order of months or years,
    this class should be used directly. Otherwise, the Calendar class should be
    used.
    """
    minutesInHour = 60
    secondsInMinute = 60

    def __init__(self, hours=None, minutes=None, seconds=None):
        now = datetime.now()
        if hours == None:
            hours = now.hour
        if minutes == None:
            minutes = now.minute
        if seconds == None:
            seconds = now.second + now.microsecond / 1000000.
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __repr__(self):
        return "%s(%s, %s, %s)" % (
            self.__class__.__name__, self.hours, self.minutes, self.seconds)

    def __sub__(self, other):
        self._symmetryCheck(other)
        return self.asSeconds() - other.asSeconds()

    def __add__(self, other):
        self._symmetryCheck(other)
        return self.asSeconds() + other.asSeconds()

    def _symmetryCheck(self, other):
        pass

    def asSeconds(self):
        return (
            (self.hours * self.minutesInHour * self.secondsInMinute) +
            (self.minutes * self.secondsInMinute) + 
            self.seconds)

    @staticmethod
    def now():
        return Time(*datetime.now().timetuple()[3:3])


# XXX needs unit tests
class Month(object):
    """
    If a game needs to have customized months in its calendar, a month instance
    should be defined for each month in the year.

    @param name: the name of the month.
    @param startDay: the day of the year that the month starts on.
    @param days: the number of days in this month.
    """
    def __init__(self, name, startDay, days, abbrev=None):
        self.name = name
        self.abbrev = abbrev or name[0:3]
        self.startDay = startDay
        self.days = days

    def __len__(self):
        return self.days
    

class DateTime(Time):
    """
    This class is meant to be used when devising a means for measuring time on
    the scale of months and years for player characters in game.
    """
    monthsInYear = 12
    daysInMonth = 30.4375
    hoursInDay = 24
    monthDefinitions = []

    def __init__(self, year=None, month=None, day=None, hours=None,
                 minutes=None, seconds=None):
        now = datetime.now()
        if year == None:
            year = now.year
        if month == None:
            month = now.month
        if day == None:
            day = now.day
        if hours > self.hoursInDay:
            days, hours = divmod(hours, self.hoursInDay)
            day += days
        # This next is obviously imprecise for fractional daysInMonth.
        if day > ceil(self.daysInMonth):
            months, day = divmod(day, ceil(self.daysInMonth))
            month += months
        if month > self.monthsInYear:
            years, month = divmod(month, self.monthsInYear)
            year += years
        self.year = year
        self.month = month
        self.day = int(day)
        super(DateTime, self).__init__(
            hours=hours, minutes=minutes, seconds=seconds)

    def __repr__(self):
        return "%s(%s, %s, %s, %s, %s, %s)" % (
            self.__class__.__name__, self.year, self.month, self.day,
            self.hours, self.minutes, self.seconds)

    def _symmetryCheck(self, other):
        isException = False
        if self.monthsInYear != other.monthsInYear:
            isException = True
        if self.monthsInYear != other.monthsInYear:
            isException = True
        if self.monthsInYear != other.monthsInYear:
            isException = True
        if isException:
            msg = ("There is a mismatch between the two time objects. "
                   "In order to perform mathematical operations on two "
                   "time objects, month, day, and hour counts must match.")
            raise TypeError(msg)

    def _getYearSeconds(self):
        return (
            self.monthsInYear * self.daysInMonth * 
            self.hoursInDay * realHour)

    def _getMonthSeconds(self):
        return self.daysInMonth * self.hoursInDay * realHour

    def _getDaySeconds(self):
        return self.hoursInDay * realHour

    def asSeconds(self):
        yearSeconds = self.year * self._getYearSeconds()
        monthSeconds = self.month * self._getMonthSeconds()
        daySeconds = self.day * self._getDaySeconds()
        seconds = yearSeconds + monthSeconds + daySeconds
        return super(DateTime, self).asSeconds() + int(seconds)

    def fromSeconds(self, seconds):
        year, remainder = divmod(seconds, self._getYearSeconds())
        month, remainder = divmod(remainder, self._getMonthSeconds())
        day, remainder = divmod(remainder, self._getDaySeconds())
        hours, remainder = divmod(remainder, realHour)
        minutes, seconds = divmod(remainder, realMinute)
        args = [int(x) for x in [year, month, day, hours, minutes, seconds]]
        return self.__class__(*args)

    # XXX add a unit test for this
    def getDaysInMonth(self):
        monthObject = self.getMonthObject()
        if monthObject:
            return monthObject.days
        return self.daysInMonth

    # XXX add a unit test for this
    def daysInYear(self):
        if self.monthDefinitions:
            return sum([x.days for x in self.monthDefinitions])
        return self.monthsInYear * self.daysInMonth

    # XXX add a unit test for this
    def getMonthObject(self):
        if self.monthDefinitions:
            return self.monthDefinitions[self.month - 1]

    # XXX add a unit test for this
    def getMonthName(self, short=False):
        month = self.getMonthObject()
        if month:
            if short:
                return month.abbrev
            return month.name
        month = datetime(1900, self.month, 1)
        if short:
            return month.strftime("%b")
        return month.strftime("%B")

    def getFriendlyDate(self, useWeeks=False):
        if not useWeeks:
            format = "the %s day of %s, year %s"
            date = format % (
                getOrdinal(self.day), self.getMonthName(), self.year)
        return date

    @staticmethod
    def now():
        now = datetime.now()
        tuple = datetime.now().timetuple()
        args = datetime.now().timetuple()[0:6]
        return DateTime(*args)


# XXX needs unit tests
class Season(object):
    """
    A season object is intended to be used as part of a collection of season
    objects. It is used to calculate local temperatures, select weather
    patterns for a given span of time, and to determine the amount of daylight
    available.
    """
    def __init__(self, name, startTime, endTime, dominentWeather=None,
                 averageTemp=None, recordHighTemp=None, recordLowTemp=None,
                 forbiddenWeather=None):
        self.name = name
        self.dominentWeather = dominentWeather
        self.forbiddenWeather = forbiddenWeather or []
        self.averageTemp = averageTemp
        self.recordHighTemp = recordHightTemp
        self.recordLowTemp = recordLowTemp


class Calendar(object):
    """
    This class is intended to be used anywhere the Time or DateTime classes are
    used. It provides a means of setting the date and/or time, and as such,
    firing off arbitrary events at desired time changes.
    """
    def __init__(self, world=None, timeClass=DateTime, timeInstance=None,
                 seasons=None, *args, **kwds):
        self.world = world
        if timeClass:
            timeInstance = timeClass(*args, **kwds)
        self.time = timeInstance
        self.lastTime = None
        self.scales = [
            (TimeScale.second, realSecond),
            (TimeScale.minute, realMinute),
            (TimeScale.hour, realHour),
            (TimeScale.day, self.time.hoursInDay * realHour),
            (TimeScale.month, (
                self.time.daysInMonth * self.time.hoursInDay * realHour)),
            (TimeScale.year, (
                self.time.daysInYear() * self.time.hoursInDay * realHour))]
        self._eventData = {}
        # XXX define dusk/dawn change points
        self.dusk = None
        self.dawn = None
        # XXX define seasons
        self.seasons = seasons

    def _getTimeScale(self, delta):
        """
        A private method for determining the order of magnitude of the
        difference between two times.
        """
        delta = abs(delta)
        lastScaleName = self.scales[0][0]
        lastScale = self.scales[0][1]
        for scaleName, scale in self.scales[1:]:
            units, seconds = divmod(delta, scale)
            if units == 0:
                return (lastScaleName, lastScale)
            lastScaleName = scaleName
            lastScale = scale
        return (scaleName, scale)

    def _getTimeChangeType(self):
        """
        A private method for determining types of time changes between the last
        time increment and the current one.
        """
        # Define non-changes.
        noYearChange = self.lastTime.year == self.time.year
        noMonthChange = self.lastTime.month == self.time.month
        noDayChange = self.lastTime.day == self.time.day
        noHourChange = self.lastTime.hours == self.time.hours
        # Define changes.
        yearChange = self.lastTime.year != self.time.year
        monthChange = self.lastTime.month != self.time.month
        dayChange = self.lastTime.day != self.time.day
        dawnChange = self.lastTime < self.dawn <= self.time
        duskChange = self.lastTime < self.dusk <= self.time
        hourChange = self.lastTime.hours != self.time.hours
        # Do time change checks.
        if hourChange and noYearChange and noMonthChange and noDayChange:
            return TimeChange.hour
        if dawnChange and noYearChange and noMonthChange and noDayChange:
            return TimeChange.dawn
        if duskChange and noYearChange and noMonthChange and noDayChange:
            return TimeChange.dusk
        elif dayChange and noYearChange and noMonthChange:
            return TimeChange.day
        elif monthChange and noYearChange:
            return TimeChange.month
        elif yearChange:
            return TimeChange.year

    def setTimeEvent(self, name, eventClass, subscriberInstance):
        """
        Set the event object for the given time scale. On a time-scale change
        that matches the given scale, the event subscribers will be notified.
        """
        self._eventData[name] = eventClass
        subscribe(subscriberInstance, eventClass)

    def getTimeEvent(self, scale):
        return self._eventData.get(scale)

    def setTime(self, newTime):
        self.lastTime = self.time
        self.time = newTime
        delta = self.time - self.lastTime
        scaleName, scale = self._getTimeScale(delta)
        # Fire off any time-scale events that have been registered.
        event = self.getTimeEvent(scaleName)
        if event:
            notify(event)
        changeName = self._getTimeChangeType()
        # Fire off any time-change events that have been registered.
        eventClass = self.getTimeEvent(changeName)
        if eventClass:
            notify(eventClass(self.world.player, self))

    def setWorld(self, world):
        self.world = world

    def getCurrentSeason(self):
        pass
