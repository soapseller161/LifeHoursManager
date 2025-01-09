import os

import constants
from utilclasses import Attribute


class ConfigManager:
    def __init__(self):
        self.__attributes = []
        self.__is_loaded = False
        self.load()

    def load(self) -> None:
        save_file_path = f"{constants.CONFIG_FILE_NAME}.txt"

        if not os.path.exists(save_file_path):
            print(f"Config file does not exist. Creating one...")
            file = open(save_file_path, 'w', encoding='utf-8')
            file.write("<str attribute>, <int weekly norm>; No empty lines in file.")
            file.close()

        try:
            file_lines = open(save_file_path, 'r', encoding='utf-8').readlines()
        except Exception as ex:
            print(f"{constants.RED}Failed to open config file: {ex}{constants.RESET}")
            return

        file_lines.pop(0)

        try:
            for line in file_lines:
                split = line.split(',')
                line_name = split[0]
                line_norm = int(split[1])
                self.__attributes.append(Attribute(name=line_name, norm=line_norm))
        except Exception as ex:
            print(f"{constants.RED}Failed to parse config file: {ex}{constants.RESET}")
            return

        self.__is_loaded = True
        print(f"{constants.GREEN}Config file parsed successfully;{constants.RESET} "
              f"loaded <{len(self.__attributes)}> attributes")

    def get_attributes_names(self) -> [str]:
        names = []

        for attribute in self.__attributes:
            names.append(attribute.name)

        return names

    def get_norm_by_name(self, name: str) -> int:
        for attribute in self.__attributes:
            if attribute.name == name:
                return attribute.norm

    @property
    def was_loaded_successfully(self):
        return self.__is_loaded

    @property
    def attributes(self):
        return self.__attributes

