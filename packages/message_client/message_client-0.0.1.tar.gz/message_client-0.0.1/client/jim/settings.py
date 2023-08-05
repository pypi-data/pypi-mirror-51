# Общие параметры
ENCODING = 'utf-8'

# Параметры серверного скрипта
IP_SERVER_DEFAULT = ''
PORT_SERVER_DEFAULT = 7777

# Параметры клиентского скрипта
IP_CLIENT_DEFAULT = '127.0.0.10'
PORT_CLIENT_DEFAULT = 7777


PATTERN_IP = r'^([0-9]|[0-9][0-9]|[0-1][0-9][0-9]|25[0-5])\.' \
             r'([0-9]|[0-9][0-9]|[0-1][0-9][0-9]|25[0-5])\.' \
             r'([0-9]|[0-9][0-9]|[0-1][0-9][0-9]|25[0-5])\.' \
             r'([0-9]|[0-9][0-9]|[0-1][0-9][0-9]|25[0-5])$'


ERROR_LIST_1 = {
    '100': 100,
    '101': 101,
    '200': 200,
    '201': 201,
    '202': 202,
    '400': 400,
    '401': 401,
    '402': 402,
    '403': 403,
    '404': 404,
    '409': 409,
    '410': 410,
    '500': 500
}

# Коды ответов сервера
ERROR_LIST = {
    '100': 'базовое уведомление',
    '101': 'важное уведомление',
    '200': 'OK',
    '201': '(created) - объект создан',
    '202': '(accepted) - подтверждение',
    '400': 'неправильный запрос/JSON-объект',
    '401': 'не авторизован',
    '402': 'неправильный логин/пароль',
    '403': '(forbidden) - пользователь заблокирован',
    '404': '(not found) - пользователь/чат отсутствует на сервере',
    '409': '(conflict) - уже имеется подключение с указанным логином',
    '410': '(gone) - адресат существует, но недоступен',
    '500': 'ошибка сервера'
}


# Сообщение для авторизации
MESSAGE_AUTHENTICATE = {
    'action': 'authenticate',
    'time': '',
    'user': {
        'account_name': 'CodeMaver1ck',
        'password': 'CorrectHorseBatteryStaple'
    }
}

# Сообщение отключение от сервера
MESSAGE_QUIT = {
    'action': 'quit'
}

# Сообщение о присутствии
MESSAGE_PRESENCE = {
    'action': 'presence',
    'time': '',
    'type': 'status',
    'user': {
        'account_name': 'CddeMaver1ck',
        'status': 'Yep, I am here!'
    }
}


# Сообщение пользователю
MESSAGE_CLIENT_CLIENT = {
    'action': 'msg',
    'time': '',
    'to': 'account_name',
    'from': 'account_name',
    'encoding': ENCODING,
    'message': 'message'
}

# Сообщение в чат
CLIENT_CHAT_MESSAGE = {
    'action': 'msg',
    'time': '',
    'to': '#room_name',
    'from': 'account_name',
    'message': 'Hello World'
}

# Присоединиться к чату
CLIENT_CHAT_JOIN = {
    'action': 'join',
    'time': '',
    'room': '#room_name'
}

# Покинуть чат
CLIENT_CHAT_LEAVE = {
    'action': 'leave',
    'time': '',
    'room': '#room_name'
}





# # Ответ сервера клиенту при авторизации
# MESSAGE_RESPONSE_ALERT = {
#     'response': 200,
#     'alert': ''
# }
#
# MESSAGE_RESPONSE_ERROR = {
#     'response': 402,
#     'error': ''
# }


# Проверка доступности пользователя online
MESSAGE_PROBE = {
    'action': 'probe',
    'time': ''
}

# Сообщение-ответ сервера при коде ответа 1xx/2xx
MESSAGE_ALERT = {
    'response': '',
    'time': '',
    'alert': ''
}

# Сообщение-ответ сервера при коде ответа 4xx/5xx
MESSAGE_ERROR = {
    'response': '',
    'time': '',
    'error': ''
}








