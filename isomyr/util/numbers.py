def getOrdinal(number):
    if 10 <= number % 100 < 20:
        return str(number) + 'th'
    else:
        ordinals = {1 : 'st', 2 : 'nd', 3 : 'rd'}
        default = "th"
        return str(number) + ordinals.get(number % 10, default)
