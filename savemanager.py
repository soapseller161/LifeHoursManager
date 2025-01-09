import constants
import os
from datetime import datetime, date, timedelta
from utilclasses import Note, Week, Attribute


class SaveManager:
    def __init__(self):
        self.__notes = []
        self.__is_loaded = False
        self.load()

    def load(self) -> None:
        save_file_path = f"{constants.SAVE_FILE_NAME}.txt"

        if not os.path.exists(save_file_path):
            print(f"Save file does not exist. Creating one...")
            file = open(f'{constants.SAVE_FILE_NAME}.txt', 'w', encoding='utf-8')
            file.write("YYYY-MM-DD, <str attribute>, <int value>, <str note>; No empty lines in file.")
            file.close()

        try:
            file_lines = open(f'{constants.SAVE_FILE_NAME}.txt', 'r', encoding='utf-8').readlines()
        except Exception as ex:
            print(f"{constants.RED}Failed to open save file: {ex}{constants.RESET}")
            return

        file_lines.pop(0)

        try:
            for line in file_lines:
                split = line.split(',')
                line_date_str = split[0]
                line_date = datetime.strptime(line_date_str, "%Y-%m-%d")
                line_date = line_date.date()
                line_attribute = split[1]
                line_value = int(split[2])

                if len(split) > 3:
                    line_note = str(split[3])
                else:
                    line_note = ""

                self.__notes.append(Note(attribute=line_attribute, value=line_value, note_date=line_date,
                                         note=line_note))
        except Exception as ex:
            print(f"{constants.RED}Failed to parse save file: {ex}{constants.RESET}")
            return

        self.__is_loaded = True
        print(f"{constants.GREEN}Save file parsed successfully;{constants.RESET} loaded <{len(self.__notes)}> notes")

    def get_attribute_notes(self, attribute: str, timedelta_in_days: int) -> [Note]:
        result = []
        start_date = datetime.today() - timedelta(days=timedelta_in_days)
        start_date = start_date.date()

        for note in self.__notes:
            if note.date >= start_date and note.attribute == attribute:
                result.append(note)

        return result

    def get_week_notes(self) -> [Note]:
        result = []
        week_start_date = Week.get_current_week_start()

        for note in self.__notes:
            if note.date >= week_start_date:
                result.append(note)

        return result

    def get_week_breakdown(self, attributes: [Attribute]) -> str:
        weekday = date.today().weekday()
        message = f"\n{Week.get_current_week_repr()} breakdown:\n"

        for attribute in attributes:
            attribute_sum = 0
            notes_count = 0

            for note in self.get_attribute_notes(attribute=attribute.name, timedelta_in_days=weekday):
                attribute_sum += note.value
                notes_count += 1

            if attribute_sum < attribute.norm:
                attribute_color = constants.YELLOW
            else:
                attribute_color = constants.GREEN

            attribute_breakdown = (f"\t{attribute_color}{attribute.name}: {attribute_sum}/{attribute.norm}"
                                   f"{constants.RESET}")

            if notes_count > 0:
                attribute_breakdown += f", {round(attribute_sum/notes_count)} avg"

            attribute_breakdown += "\n"

            message += attribute_breakdown

        return message

    def get_week_notes_repr(self) -> str:
        message = f"\n{Week.get_current_week_repr()} summary:"
        week_notes = self.get_week_notes()

        for week_note in week_notes:
            message += f"\n\t{week_note}"

        message += f"\nTotal notes: <{len(week_notes)}>\n"
        return message

    def write_note(self, note: Note):
        with open(f'{constants.SAVE_FILE_NAME}.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{note.date},{note.attribute},{note.value}")
        file.close()
        self.__notes.append(note)

    @property
    def was_loaded_successfully(self):
        return self.__is_loaded
