class Password_Error(Exception):
    pass


class Login_error(Exception):
    pass


class MyFileNotFoundError(FileNotFoundError):
    def __str__(self):
        return 'Неверный путь или название файла'


class Len_Pass_Error(Password_Error):
    def __str__(self):
        return 'Пароль должен быть более 8 симолов'


class User_Error(Login_error):
    def __str__(self):
        return 'Такой логин уже занят'


class Len_Username_Error(Login_error):
    def __str__(self):
        return 'Длина логина не должна быть меньше 4!'


class Incorrect_Enter(Exception):
    def __str__(self):
        return 'Неправильное имя пользователя или пароль.\nПовторите попытку'


class Space_Error(Exception):
    def __str__(self):
        return 'Вы заполнили не все поля'


class Olymp_Error(Exception):
    def __str__(self):
        return "Уже есть такая олимпиада!"


class Space_Olympiad_Error(Exception):
    def __str__(self):
        return 'Обязательно пропишите название и предмет олимпиады'
