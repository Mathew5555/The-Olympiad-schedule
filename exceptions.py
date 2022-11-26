from messages_box import *


class Password_Error(Exception):
    pass


class Len_Error(Password_Error):
    def __init__(self, title, text):
        warning_message_box(self, title, text)


class User_Error(Exception):
    def __str__(self):
        return 'Такой логин уже занят'


class Len_Username_Error(Exception):

    def __str__(self):
        return 'Длина логина не должна быть меньше 4!'
