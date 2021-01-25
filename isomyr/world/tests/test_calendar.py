from datetime import datetime
from unittest import TestCase

from isomyr.world import calendar


class GameSpeedTestCase(TestCase):

    def test_speeds(self):
        self.assertEquals(calendar.SPEED_10, 105120)
        self.assertEquals(calendar.SPEED_09, 8760)
        self.assertEquals(calendar.SPEED_08, 2190)
        self.assertEquals(calendar.SPEED_07, 1440)
        self.assertEquals(calendar.SPEED_06, 672)
        self.assertEquals(calendar.SPEED_05, 360)
        self.assertEquals(calendar.SPEED_04, 168)
        self.assertEquals(calendar.SPEED_03, 72)
        self.assertEquals(calendar.SPEED_02, 30)
        self.assertEquals(calendar.SPEED_01, 12)
        self.assertEquals(calendar.SPEED_00, 1)


class TimeTestCase(TestCase):

    def test_creationDefaults(self):
        now = calendar.Time()
        self.assertTrue(isinstance(now.seconds, float))

    def test_creation(self):
        now = calendar.Time(23, 14, 47)
        self.assertEquals(now.hours, 23)
        self.assertEquals(now.minutes, 14)
        self.assertEquals(now.seconds, 47)

    def test_repr(self):
        now = calendar.Time(23, 14, 47)
        self.assertEquals(repr(now), "Time(23, 14, 47)")

    def test_subtraction(self):
        earlier = calendar.Time()
        later = calendar.Time()
        sub1 = later - earlier
        self.assertTrue(0 < sub1 < 1)
        sub2 = earlier - later
        self.assertTrue(-1 < sub2 < 0)

    def test_addition(self):
        earlier = calendar.Time()
        later = calendar.Time()
        self.assertTrue(earlier + later > 1)

    def test_asSeconds(self):
        now = calendar.Time(23, 14, 47)
        expectedSeconds = 23 * 60 * 60 + 14 * 60 + 47
        self.assertEquals(now.asSeconds(), expectedSeconds)


class DateTimeTestCase(TestCase):

    def test_creationDefaults(self):
        now = calendar.DateTime()
        datetimeNow = datetime.now()
        expected = datetime(now.year, now.month, now.day, now.hours,
                            now.minutes, int(now.seconds))
        delta = datetimeNow - expected
        self.assertTrue(delta.seconds < 1)

    def test_creation(self):
        now = calendar.DateTime(2038, 1, 1, 0, 0, 0)
        self.assertEquals(now.year, 2038)
        self.assertEquals(now.month, 1)
        self.assertEquals(now.day, 1)
        self.assertEquals(now.hours, 0)
        self.assertEquals(now.minutes, 0)
        self.assertEquals(now.seconds, 0)

    def test_symmetryCheck(self):
        earlier = calendar.DateTime(1999, 12, 31, 23, 59, 59)

        class CustomDateTime(calendar.DateTime):
            monthsInYear = 14
            daysInMonth = 49
            hoursInDay = 32

        later = CustomDateTime(2000, 1, 1, 0, 0, 0)
        self.assertRaises(TypeError, lambda: later - earlier)

    def test_subtraction(self):
        earlier = calendar.DateTime()
        later = calendar.DateTime()
        sub1 = later - earlier
        self.assertTrue(0 < sub1 < 1)
        sub2 = earlier - later
        self.assertTrue(-1 < sub2 < 0)

    def test_addition(self):
        earlier = calendar.DateTime()
        later = calendar.DateTime()
        self.assertTrue(earlier + later > 1)

    def test_overHours(self):
        now = calendar.DateTime(2038, 12, 31, 72, 0, 0)
        self.assertEquals(now.year, 2039)
        self.assertEquals(now.month, 1)
        self.assertEquals(now.day, 3)

    def test_overDays(self):
        now = calendar.DateTime(2038, 12, 32, 0, 0, 0)
        self.assertEquals(now.year, 2039)
        self.assertEquals(now.month, 1)
        self.assertEquals(now.day, 1)

    def test_overMonths(self):
        now = calendar.DateTime(2038, 14, 1, 0, 0, 0)
        self.assertEquals(now.year, 2039)
        self.assertEquals(now.month, 2)

    def test_repr(self):
        now = calendar.DateTime(2038, 1, 1, 0, 0, 0)
        self.assertEquals(repr(now), "DateTime(2038, 1, 1, 0, 0, 0)")

    def test_asSeconds(self):
        now = calendar.DateTime(2038, 1, 1, 23, 14, 47)
        expectedSeconds = (
            2038 * 365.25 * 24 * 60 * 60 +
            1 * 30.4375 * 24 * 60 * 60 +
            1 * 24 * 60 * 60 +
            23 * 60 * 60 +
            14 * 60 +
            47)
        self.assertEquals(now.asSeconds(), expectedSeconds)

    def test_fromSeconds(self):
        seconds = 249000
        result = calendar.DateTime().fromSeconds(seconds)
        self.assertEquals(repr(result), "DateTime(0, 0, 2, 21, 10, 0)")
        result = calendar.DateTime().fromSeconds(63427220661.125893)
        self.assertEquals(repr(result), "DateTime(2009, 10, 19, 17, 24, 21)")

    def test_daysInYear(self):
        now = calendar.DateTime()
        self.assertEquals(now.daysInYear(), 365.25)


class CustomDateTime(calendar.DateTime):

    monthsInYear = 14
    daysInMonth = 49
    hoursInDay = 32
    monthDefinitions = [
        calendar.Month("Bidan", 148, 49, "abbr"),
        calendar.Month("Sniwdig", 1, 49, "abbr"),
        calendar.Month("Hreran", 50, 49, "abbr"),
        calendar.Month("Windig", 197, 49, "abbr"),
        calendar.Month("Cennen", 99, 49, "abbr"),
        calendar.Month("Lafian", 295, 49, "abbr"),
        calendar.Month("Laedan", 246, 49, "abbr"),
        calendar.Month("Leohtig", 344, 49, "abbr"),
        calendar.Month("Gledig", 393, 49, "abbr"),
        calendar.Month("Calan", 491, 49, "abbr"),
        calendar.Month("Wistecir", 442, 49, "abbr"),
        calendar.Month("Breccig", 589, 49, "abbr"),
        calendar.Month("Cruncon", 540, 49, "abbr"),
        calendar.Month("Freorig", 638, 49, "abbr")]

class CustomDateTimeTestCase(TestCase):

    def setUp(self):
        self.now = CustomDateTime(803, 13, 49, 31, 59, 17)

    def test_asSeconds(self):
        expectedSeconds = (
            803 * 686 * 32 * 60 * 60 +
            13 * 49 * 32 * 60 * 60 +
            49 * 32 * 60 * 60 +
            31 * 60 * 60 +
            59 * 60 +
            17)
        self.assertEquals(self.now.asSeconds(), expectedSeconds)

    def test_daysInYear(self):
        self.assertEquals(self.now.daysInYear(), 686)

    def test_getDaysInMonth(self):
        self.assertEquals(self.now.getDaysInMonth(), 49)

    def test_getMonthName(self):
        self.assertEquals(self.now.getMonthName(), "Cruncon")

    def test_getFriendlyDate(self):
        self.assertEquals(
            self.now.getFriendlyDate(),
            "the 49th day of Cruncon, year 803")
        date = CustomDateTime(3144, 1, 37, 31, 59, 17)
        self.assertEquals(
            date.getFriendlyDate(),
            "the 37th day of Bidan, year 3144")

class CalendarTestCase(TestCase):

    def test_creationDefaults(self):
        cal = calendar.Calendar()
        self.assertTrue(isinstance(cal.time, calendar.DateTime))

    def test_getTimeScaleForYears(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30)
        nextTime = calendar.DateTime(2009, 10, 19, 10, 58)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.year)

    def test_getTimeScaleForMonths(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30)
        nextTime = calendar.DateTime(1973, 7, 19, 10, 58)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.month)

    def test_getTimeScaleForDays(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30)
        nextTime = calendar.DateTime(1972, 9, 16, 10, 58)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.day)

    def test_getTimeScaleForHours(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30)
        nextTime = calendar.DateTime(1972, 8, 16, 10, 58)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.hour)

    def test_getTimeScaleForMinutes(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30)
        nextTime = calendar.DateTime(1972, 8, 17, 3, 58)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.minute)

    def test_getTimeScaleForSeconds(self):
        cal = calendar.Calendar(
            year=1972, month=8, day=17, hours=4, minutes=30, seconds=24)
        nextTime = calendar.DateTime(1972, 8, 17, 4, 30, 19)
        delta = nextTime - cal.time
        scaleName, scale = cal._getTimeScale(delta)
        self.assertEquals(scaleName, calendar.TimeScale.second)

    def test_setTimeEvent(self):

        class MyEvent(object):
            pass

        class MySubscriber(object):
            pass

        cal = calendar.Calendar()
        cal.setTimeEvent(calendar.TimeScale.day, MyEvent, MySubscriber())
        self.assertEquals(cal._eventData[calendar.TimeScale.day], MyEvent)

    def test_getTimeEvent(self):

        class MyEvent(object):
            pass

        class MySubscriber(object):
            pass

        cal = calendar.Calendar()
        cal.setTimeEvent(calendar.TimeScale.day, MyEvent, MySubscriber())
        self.assertEquals(cal.getTimeEvent(calendar.TimeScale.day), MyEvent)

    def test_setTime(self):
        cal = calendar.Calendar()
        originalTime = cal.time
        nextMoment = calendar.DateTime()
        cal.setTime(nextMoment)
        self.assertEquals(cal.lastTime, originalTime)
        # XXX add more testing for more code (code that's not written yet)


class SeasonsTestCase(TestCase):

    def setUp(self):
        super(SeasonsTestCase, self).setUp()

