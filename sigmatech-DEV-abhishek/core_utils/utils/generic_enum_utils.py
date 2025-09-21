import enum


class EnumChoices(enum.Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
