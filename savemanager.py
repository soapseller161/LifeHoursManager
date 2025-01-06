import constants
import os
from datetime import datetime, date, timedelta
from utilclasses import Note


class SaveManager:
    def __init__(self):
        self.__notes = []
        self.__is_loaded = False
        self.load()

    def load(self) -> None:
        save_file_path = f"{constants.save_file_name}.txt"

        if not os.path.exists(save_file_path):
            print(f"Save file does not exist. Creating one...")
            file = open(f'{constants.save_file_name}.txt', 'w', encoding='utf-8')
            file.write("YYYY-MM-DD, <str attribute>, <int value>")
            file.close()

        try:
            file_lines = open(f'{constants.save_file_name}.txt', 'r', encoding='utf-8').readlines()
        except Exception as ex:
            print(f"Failed to open save file: {ex}")
            return

        file_lines.pop(0)

        try:
            for line in file_lines:
                split = line.split(',')
                line_date_str = split[0]
                line_date = datetime.strptime(line_date_str, "%Y-%m-%d")
                line_attribute = split[1]
                line_value = int(split[2])
                self.__notes.append(Note(attribute=line_attribute, value=line_value, note_date=line_date))
        except Exception as ex:
            print(f"Failed to parse save file: {ex}")
            return

        self.__is_loaded = True
        print(f"Save file parsed successfully; loaded <{len(self.__notes)}> notes")

    def get_attribute_notes(self, attribute: str, timedelta_in_days: int) -> [Note]:
        result = []
        start_date = datetime.today() - timedelta(days=timedelta_in_days)
        start_date = datetime.combine(start_date, datetime.min.time())

        for note in self.__notes:
            if note.date >= start_date and note.attribute == attribute:
                result.append(note)

        return result

    def get_week_breakdown(self) -> str:
        today = date.today()
        weekday = today.weekday()
        start_of_week = today - timedelta(days=weekday)
        end_of_week = start_of_week + timedelta(days=6)
        month_name = today.strftime("%B")
        message = f"\nWeek {start_of_week.day} - {end_of_week.day} of {month_name}, {end_of_week.year} breakdown:\n"

        for attribute in constants.attributes:
            attribute_sum = 0
            notes_count = 0

            for note in self.get_attribute_notes(attribute=attribute, timedelta_in_days=weekday):
                attribute_sum += note.value
                notes_count += 1

            attribute_breakdown = f"\t{attribute}: {attribute_sum}, {notes_count} notes"

            if notes_count > 0:
                attribute_breakdown += f", {round(attribute_sum/notes_count)} avg"

            attribute_breakdown += "\n"

            message += attribute_breakdown

        return message

    def write_note(self, note: Note):
        with open(f'{constants.save_file_name}.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{note.date},{note.attribute},{note.value}")
        file.close()
        self.__notes.append(note)

    @property
    def was_loaded_successfully(self):
        return self.__is_loaded
