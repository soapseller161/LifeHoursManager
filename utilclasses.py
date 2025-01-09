from datetime import date, timedelta, datetime


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
    def __init__(self, attribute: str, value: int, note_date: date, note: str):
        self.__attribute = attribute
        self.__value = value
        self.__date = note_date
        self.__note = note

    def __str__(self):
        return f"{self.__date.strftime('%A')}: {self.__attribute} {self.__value} {self.__note}"

    @property
    def attribute(self):
        return self.__attribute

    @property
    def value(self):
        return self.__value

    @property
    def date(self) -> date:
        return self.__date

    @property
    def note(self):
        return self.__note


class Week:
    @staticmethod
    def get_current_week_start() -> date:
        today = date.today()
        weekday = today.weekday()
        start_date = today - timedelta(days=weekday)
        start_date = datetime.combine(start_date, datetime.min.time())
        start_date = start_date.date()
        return start_date

    @staticmethod
    def get_current_week_end() -> date:
        return Week.get_current_week_start() + timedelta(days=6)

    @staticmethod
    def get_current_week_repr() -> str:
        today = date.today()
        start_of_week = Week.get_current_week_start()
        end_of_week = Week.get_current_week_end()
        month_name = today.strftime("%B")
        return f"Week {start_of_week.day} - {end_of_week.day} of {month_name}, {end_of_week.year}"


class Attribute:
    def __init__(self, name: str, norm: int):
        self.__name = name
        self.__norm = norm

    @property
    def name(self):
        return self.__name

    @property
    def norm(self):
        return self.__norm
