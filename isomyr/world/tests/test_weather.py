from unittest import TestCase

from isomyr.exceptions import InvalidDewPoint
from isomyr.world import weather


class TemperatureTestCase(TestCase):

    def setUp(self):
        # XXX build scene
        pass

    def test_getTemperature(self):
        pass

    def test_getCelsius(self):
        self.assertEquals(round(weather.getCelsius(98.6)), 37)
        self.assertEquals(round(weather.getCelsius(32)), 0)
        self.assertEquals(round(weather.getCelsius(0)), -18)
        self.assertEquals(round(weather.getCelsius(-40)), -40)
        self.assertEquals(round(weather.getCelsius(-459.67)), -273)

    def test_getFahrenheit(self):
        self.assertEquals(round(weather.getFahrenheit(100)), 212)
        self.assertEquals(round(weather.getFahrenheit(0)), 32)
        self.assertEquals(round(weather.getFahrenheit(-40)), -40)
        self.assertEquals(round(weather.getFahrenheit(-273)), -459)

    def test_getHeatIndex(self):
        self.assertEquals(round(weather.getHeatIndex(32, 40)), 33)
        self.assertEquals(round(weather.getHeatIndex(32, 60)), 37)
        self.assertEquals(round(weather.getHeatIndex(32, 90)), 47)
        self.assertEquals(round(weather.getHeatIndex(42, 40)), 54)
        self.assertEquals(round(weather.getHeatIndex(42, 60)), 70)
        self.assertEquals(round(weather.getHeatIndex(42, 90)), 103)

    def test_getWindChill(self):
        self.assertEquals(round(weather.getWindChill(0, 6)), -2)
        self.assertEquals(round(weather.getWindChill(0, 70)), -9)
        self.assertEquals(round(weather.getWindChill(0, 110)), -11)
        self.assertEquals(round(weather.getWindChill(-60, 6)), -70)
        self.assertEquals(round(weather.getWindChill(-60, 70)), -93)
        self.assertEquals(round(weather.getWindChill(-60, 110)), -98)


class DewPointTestCase(TestCase):

    def test_getDewPoint(self):
        self.assertEquals(round(weather.getDewPoint(1, 99)), 1)
        self.assertEquals(round(weather.getDewPoint(32, 25)), 9)
        self.assertEquals(round(weather.getDewPoint(32, 50)), 20)
        self.assertEquals(round(weather.getDewPoint(59, 3.5)), 1)
        self.assertEquals(round(weather.getDewPoint(59, 64)), 50)

    def test_lowTemp(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 0, 99)
        try:
            weather.getDewPoint(0, 99)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Temperature out of range.")

    def test_highTemp(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 100, 99)
        try:
            weather.getDewPoint(100, 99)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Temperature out of range.")

    def test_lowHumidity(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 32, 1)
        try:
            weather.getDewPoint(32, 1)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Humidity is out of range.")

    def test_highHumidity(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 32, 100)
        try:
            weather.getDewPoint(32, 100)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Humidity is out of range.")

    def test_lowDewPoint(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 59, 2)
        try:
            weather.getDewPoint(59, 2)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Computed dew point is too low.")

    def test_highDewPoint(self):
        self.assertRaises(InvalidDewPoint, weather.getDewPoint, 59, 65)
        try:
            weather.getDewPoint(59, 65)
        except InvalidDewPoint, error:
            self.assertEquals(error.message, "Computed dew point is too high.")


class WindTestCase(TestCase):

    def test_getWindType(self):
        speeds = [0, 1, 4, 7, 12, 19, 24, 31, 38, 46, 54, 63, 72, 98, 114, 131,
                  170, 200, 300, 600, 900]
        names = ["calm", "calm", "light air", "light breeze", "gentle breeze",
                 "moderate breeze", "fresh breeze", "strong breeze",
                 "moderate gale", "fresh gale", "strong gale", "whole gale",
                 "storm", "hurricane", "cyclone", "super cyclone", "typhoon",
                 "venusian typhoon", "jovian typhoon", "neptunian typhoon",
                 "saturnian typhoon"]
        for speed, expectedName in zip(speeds, names):
            name = weather.wind.getWindType(speed)
            self.assertEquals(name, expectedName)

    def test_getRainType(self):
        rates = [0, .25, 1, 4, 16, 50, 100]
        names = ["very light", "very light", "light", "moderate", "heavy",
                 "very heavy", "extremely heavy"]
        for rate, expectedName in zip(rates, names):
            name = weather.rain.getRainType(rate)
            self.assertEquals(name, expectedName)

    def test_getSnowType(self):
        rates = [0, .25, 1, 4, 16, 50, 100]
        names = ["very light", "very light", "light", "moderate", "heavy",
                 "very heavy", "extremely heavy"]
        for rate, expectedName in zip(rates, names):
            name = weather.snow.getSnowType(rate)
            self.assertEquals(name, expectedName)


class WeatherPatternTypeTestCase(TestCase):
    pass


class WeatherPatternTestCase(TestCase):
    pass
