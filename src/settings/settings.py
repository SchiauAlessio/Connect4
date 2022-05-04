class Settings:
    def __init__(self,file_name):
        self.__file_name=file_name
        self.__content = self.__read_properties_file()

    def __read_properties_file(self):
        file_name_separator = '='
        with open(self.__file_name) as file:
            content = []
            for line in file:
                if file_name_separator in line:
                    line_content = line.split(file_name_separator)
                    current_information = line_content[1].strip()
                    content.append(current_information)
            return content

    def get_difficulty(self):
        return self.__content[0]