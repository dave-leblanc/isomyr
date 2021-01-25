import math

from isomyr.exceptions import InvalidDewPoint


def getTemperature(scene):
    """
    A temperature value for a given scene is determined by checking the
    time of day, latitude, altitude, season, hemisphere, composition of
    atmosphere, distance from local star, and size of local star.
    """
    time = scene.world.getWorldTime()
    season = time.getCurrentSeason()
    sun = scene.world.getSun()
    atmosphere = scene.world.getAtmosphere()


def getCelsius(fahrenheit):
    return (fahrenheit - 32.0) * 5.0/9.0


def getFahrenheit(celsius):
    return (celsius * 9.0/5.0) + 32.0


def getHeatIndex(temp, humidity, sunshine=0):
    """
    A utility function to get the human-apparent temperature in an
    oxygen-nitrogen atmosphere given an actual temperature, a humidity level,
    and an amount of direct sunlight. Only valid for temperatures over 26C
    (80F) and humidity levels over 40%.

    @param temp: temperature in degrees Celsius
    @param humidity: percentage relative humidity
    @param sunshine: percentage of exposure direct sun; the default is 0
        percent, or in the shade

    Note that the heat index formula used below requires degrees F, so we
    convert from C to F and then back to C.
    """
    fahr = getFahrenheit(temp)
    if fahr < 80:
        return temp
    if humidity < 40:
        return temp
    decimalSunshine = sunshine/100.0
    sunshineTempAdjustment = decimalSunshine * 15
    heatIndex = (
        16.923 + (0.185212 * fahr) + (5.37941 * humidity) -
        (0.100254 * fahr * humidity) + (0.00941695 * fahr ** 2) +
        (0.00728898 * humidity ** 2) + (0.000345372 * fahr ** 2 * humidity) -
        (0.000814971 * fahr * humidity ** 2) +
        (0.0000102102 * fahr ** 2 * humidity ** 2) -
        (0.000038646 * fahr ** 3) + (0.0000291583 * humidity ** 3) +
        (0.00000142721 * fahr ** 3 * humidity) + 
        (0.000000197483 * fahr * humidity ** 3) -
        (0.0000000218429 * fahr ** 3 * humidity ** 2) +
        (0.000000000843296 * fahr ** 2 * humidity ** 3) -
        (0.0000000000481975 * fahr ** 3 * humidity ** 3))
    return getCelsius(sunshineTempAdjustment + heatIndex)


def getWindChill(temp, windSpeed):
    """
    A utility function to get the human-apparent temperature in an
    oxygen-nitrogen atmosphere given an actual temperature and a wind speed.
    Wind chill is only valid for temperatures at or lower than 10C (50F) and
    wind speeds higher than 4.8 km/h (3 m/h).

    @param temp: temperature in degrees Celcius
    @param windSpeed: wind speed in km/h
    """
    if temp > 10:
        return temp
    if windSpeed < 4.8:
        return temp
    return (13.12 + (0.6125 * temp) - (11.37 * windSpeed ** 0.16) +
            0.3965 * temp* windSpeed ** 0.16)


def getDewPoint(temp, humidity):
    """
    A utility function to get the temperature to which an amount of air must be
    cooled in order for water vapor to condense into water. This is only valid
    for: 1) temperatures between 0C and 60C, 2) relative humidity between 1%
    and 100%, and 3) dew points between 0C and 50C.

    @param temp: temperature in degrees Celsius
    @param humidity: percentage relative humidity
    """
    if not 0 < temp < 60:
        raise InvalidDewPoint("Temperature out of range.")
    if not 1 < humidity < 100:
        raise InvalidDewPoint("Humidity is out of range.")

    a = 17.271
    b = 237.7

    def gamma(temp, humidity):
        return (a * temp) / (b + temp) + math.log(humidity/100.0)

    dewPoint = (b * gamma(temp, humidity)) / (a - gamma(temp, humidity))

    if dewPoint < 0:
        raise InvalidDewPoint("Computed dew point is too low.")
    if dewPoint > 50:
        raise InvalidDewPoint("Computed dew point is too high.")
    return dewPoint


class WeatherType(object):
    # Intensity is a three-tuple of (max, min, ave)
    intensity = (100, 0, 50)
    intensityUnits = "percent"
    rate = "cm/hour"


class Humidity(WeatherType):
    name = "humidity"
    description = "humid"
    action = "humid"

humidity = Humidity()


class Fog(WeatherType):
    """
    Fog forms when the difference between temperature and dew point is
    generally less than 2.5C or 4F.

    The fog weather pattern requires an event hander for temperature and
    humidity changes.
    """
    name = "fog"
    description = "foggy"
    action = "foggy"


class Rain(WeatherType):
    name = "rain"
    description = "rainy"
    action = "raining"
    intensityUnits = "mm / hr"
    intensity = {
        (-1, 0.25): "very light",
        (0.25, 1): "light",
        (1, 4): "moderate",
        (4, 16): "heavy",
        (16, 50): "very heavy",
        (50, 100): "extremely heavy"}

    def getRainType(self, rate):
        for range, name in self.intensity.items():
            min, max = range
            if min < rate <= max:
                return name

rain = Rain()


class Snow(Rain):
    name = "snow"
    description = "snowy"
    action = "snowing"
    intensityUnits = "cm / hr"

    def getSnowType(self, rate):
        """
        This works because 1) the snow fall is approximately 10 times the
        accumulated height as water-equivalent, and 2) the units (cm) are ten
        times the liquid equivalent (mm).
        """
        return super(Snow, self).getRainType(rate)

snow = Snow()


class Sunshine(WeatherType):
    name = "sunshine"
    description = "sunny"
    action = "sunny"

sunshine = Sunshine()


class Clouds(WeatherType):
    name = "clouds"
    description = "cloudy"
    action = "cloudy"

clouds = Clouds()


class Wind(WeatherType):
    direction = None
    intensityUnits = "mph"
    intensity = {
        (-1, 1): "calm",
        (1, 4): "light air",
        (4, 7): "light breeze",
        (7, 12): "gentle breeze",
        (12, 19): "moderate breeze",
        (19, 24): "fresh breeze",
        (24, 31): "strong breeze",
        (31, 38): "moderate gale",
        (38, 46): "fresh gale",
        (46, 54): "strong gale",
        (54, 63): "whole gale",
        (63, 72): "storm",
        (72, 98): "hurricane",
        (98, 114): "cyclone",
        (114, 131): "super cyclone",
        (131, 170): "typhoon",
        (170, 200): "venusian typhoon",
        (200, 300): "jovian typhoon",
        (300, 600): "neptunian typhoon",
        (600, 900): "saturnian typhoon",
        }

    def getWindType(self, speed):
        for range, name in self.intensity.items():
            min, max = range
            if min < speed <= max:
                return name

wind = Wind()


class WeatherPatternType(object):
    """
    A weather pattern type object is intended to be used to define a range of
    weather types that are valid under specific conditions. For example, a
    weather pattern type could be defined for selection during a particular
    time of day. Ideally, several valid weather pattern types for a specific
    condition would be defined and selected from. Selection mechanisms are left
    to the developer to create, but a weighted value attribute on a pattern
    type can be used to increase or decrease the frequency with which a
    particular pattern is selected.
    """
    def __init__(self, weatherType, intensityRange=(0, 1), weight=.5):
        pass


class WeatherPattern(object):
    """
    Intended for use with procedural weather generation, this base class is
    intended to be subclassed and ...

    A collection of weather pattern types...

    A constant that indicates the tendency of the weather to change needs to be
    defined. This changeability is a two-tuple: the first element represents
    the likelihood of change and the second element represents the time period
    (in seconds) over which that likelihood is defined.

    Each weather type class attribute should be a WeatherPatternType instance
    (or subclass instance).

    For every season, a weather pattern type should be defined, in the same
    order as the seasons are defined in the calendar.
    """
    changeability = 0
    dayTypes = []
    nightTypes = []
    seasonTypes = []
