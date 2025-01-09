import os
from datetime import date

from configmanager import ConfigManager
from savemanager import SaveManager
from utilclasses import Question, Note


class LifeHoursManager:
    def __init__(self):
        self.__save_manager = SaveManager()
        self.__config_manager = ConfigManager()

    @staticmethod
    def get_answer_to_question(question: Question) -> int:
        LifeHoursManager.ask_question(question=question)
        return LifeHoursManager.get_int_input(1, len(question.variants))

    @staticmethod
    def get_start_question() -> Question:
        variants = ["Write attribute", "Get week breakdown", "Get week notes"]

        return Question(text="What do you want?", variants=variants)

    @staticmethod
    def ask_question(question: Question):
        print(str(question))

    @staticmethod
    def get_int_input(minimum: int = None, maximum: int = None) -> int:
        while True:
            try:
                _input = int(input())

                if minimum is None and maximum is None:
                    return _input

                if minimum <= _input <= maximum:
                    return _input
                else:
                    print(f"Please, input integer between {minimum} - {maximum}")

            except ValueError:
                print("Please, input integer")

    def get_attribute_question(self) -> Question:
        return Question(text="What attribute do you choose?", variants=self.__config_manager.get_attributes_names())

    def resolve_new_request(self) -> None:
        if not self.__save_manager.was_loaded_successfully or not self.__config_manager.was_loaded_successfully:
            print("Press <Enter> to exit")
            input()
            return

        answer = self.get_answer_to_question(self.get_start_question())

        if answer == 1:
            if len(self.__config_manager.get_attributes_names()) == 0:
                print("No attributes in config file\n")
            else:
                chosen_attribute = self.__config_manager.get_attributes_names()[
                    self.get_answer_to_question(self.get_attribute_question()) - 1]
                print(f"Write value for {chosen_attribute}:")
                value = LifeHoursManager.get_int_input()
                print(f"Write note to record:")
                note = input()
                self.__save_manager.write_note(Note(attribute=chosen_attribute, value=value,
                                                    note_date=date.today(), note=note))
                print(f"Attribute <{chosen_attribute}> with value <{value}> has been written\n")
        elif answer == 2:
            print(self.__save_manager.get_week_breakdown(attributes=self.__config_manager.attributes))
        elif answer == 3:
            print(self.__save_manager.get_week_notes_repr())
        else:
            print("Answer is not supported\n")

        self.resolve_new_request()


if __name__ == '__main__':
    os.system("cls")
    manager = LifeHoursManager()
    manager.resolve_new_request()
