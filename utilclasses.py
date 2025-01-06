import constants
from datetime import date


class Question:
    def __init__(self, text: str, variants: [str]):
        self.__text = text
        self.__variants = variants

    def __str__(self):
        result = self.__text

        for i in range(len(self.__variants)):
            result += f"\n{i+1}. {self.__variants[i]}"

        return result

    @property
    def variants(self) -> [str]:
        return self.__variants


class Note:
    def __init__(self, attribute: str, value: int, note_date: date):
        self.__attribute = attribute
        self.__value = value
        self.__date = note_date

    @property
    def attribute(self):
        return self.__attribute

    @property
    def value(self):
        return self.__value

    @property
    def date(self):
        return self.__date
