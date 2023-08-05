class InvalidCodeErrorHTTP(Exception):
    """ Исключение возникающее при получении
    несуществующего кода ошибки HTTP
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'Неверный код ответа {}'.format(self.code)

