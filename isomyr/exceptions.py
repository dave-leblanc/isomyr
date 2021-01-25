class IsomyrError(Exception):

    def __str__(self):
        return self.message or self.__doc__

class ObjectNotFoundError(IsomyrError):
    """Could not find specified object."""


class DuplicateObjectError(IsomyrError):
    """An object with that name already exists."""


class SkinImageCountError(IsomyrError):
    """
    The number of skin images does not match expected values for the given
    frames per cycle.
    """


class SkinDirectionalImageError(IsomyrError):
    """The directional image isn't oriented properly."""


class SkinCycleSequenceMismatchError(IsomyrError):
    """The frame sequence length and frames per cycle do not match."""


class SkinImageCorrelationMismatchError(IsomyrError):
    """The skin has unequal image counts in different directions."""


class EventSubscriberNotFound(IsomyrError):
    """Could not find a subscriber for the given event."""


class InvalidDewPoint(IsomyrError):
    """The provided values did not produce a valid dewpoint."""
