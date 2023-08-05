from socket import *
import sys
import os
import re
import time
import logging
from threading import Thread
from PyQt5 import QtWidgets
import hashlib
import hmac
import binascii

from gui.main import *
from jim.error import *
from jim.settings import *
from jim.utils import *
from metaclasses.client_meta import *
from db.client_db import *


logger = logging.getLogger('client')


class Client(Thread, metaclass=ClientMeta):
    """
    Класс - реализующий логику работы клиентского приложения
    """

    def __init__(self, db, address, name, password, registr):
        super().__init__()
        self.db = db
        self.address = address
        self.name_client = name
        self.password = password
        self.registr = registr

    def run(self):
        """
        Метод запускающий клиента
        :return:
        """
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(self.address)
        if self.registr:
            self.registration()
        else:
            self.authorization()

        t = Thread(target=self.get_message, args=(self.sock,))
        t.daemon = True
        t.start()                    # запуск программы получения сообщений

    def registration(self):
        """
        Регистрация пользователя
        """
        print('Регистрация')
        msg = {
            'action': 'registration',
            'time': time.time(),
            'login': self.name_client,
            'password': self.password
        }
        send_message(self.sock, msg)
        print('Отправлено сообщение регистрации', msg)
        answer = receiving_message(self.sock)
        print('Получено сообщениеот сервера  о статусе регистрации', answer)
        if 'response' in answer.keys() and answer['response'] == 511:
            print('Регистрация прошла успешно')
            self.authorisation = True
            # chat_app.show()
            return
        else:
            print('Регистрация провалилась')
            self.authorisation = False
            self.error_text = answer['alert']
            # exit(0)

    def authorization(self):
        """
        Авторизация пользователя
        """
        print('Авторизация')
        msg = {
            'action': 'authorization',
            'time': time.time(),
            'login': self.name_client,
        }

        print('Отправка сообщения authorization', msg)
        send_message(self.sock, msg)
        answer = receiving_message(self.sock)

        print('Получен ответ от cервера с секретным ключем', answer)
        if answer['response'] != 500:
            print('Сервер не прислал секретный ключ')
            self.authorisation = False
            print('Авторизация не прошла')
            self.error_text = answer['alert']
            return

        password_bytes = self.password.encode('utf-8')
        salt = self.name_client.lower().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512', password_bytes, salt, 10000)
        password_hash_string = binascii.hexlify(password_hash)

        ans_data = answer['data']
        hash = hmac.new(password_hash_string, ans_data.encode('utf-8'))
        digest = hash.digest()
        data = binascii.b2a_base64(digest).decode('ascii')
        msg = {
            'response': 511,
            'data': data,
            'login': self.name_client
        }
        print('Отправка сообщения серверу с hmac-функцией', msg)
        send_message(self.sock, msg)
        answ = receiving_message(self.sock)
        print('Ответ от сервера о статусе авторизации', answ)
        if answ['response'] == '511':
            print('Авторизация прошла успешно')
            self.authorisation = True
            # chat_app.show()
            return
        else:
            self.authorisation = False
            print('Авторизация не прошла')
            self.error_text = answ['alert']
            # exit(0)

    def get_message(self, s):
        """
        Получение сообщений от сервера
        """
        while True:
            msg = receiving_message(s)
            print('msg ', msg)

            # получен список всех пользователей
            if 'action' in msg.keys() and msg['action'] == 'users_list':
                chat_app.add_user.display_users_list(msg['data'])

            elif 'action' in msg.keys() and msg['action'] == 'online_users_list':
                chat_app.add_user.display_users_list(msg['data'])

            # получен список контактов
            elif 'action' in msg.keys() and msg['action'] == 'contacts_list':
                self.db.add_contact(msg['data'])

            # получено сообщение от пользователя
            elif 'action' in msg.keys() and msg['action'] == 'msg':
                print(f'{self.name_client} получил сообщение {msg["message"]}')
                self.db.send_message(msg['message'], False, msg['from'])
                chat_app.add_msg_in_display_chat(
                    msg['message'], False, msg['from'])

            elif msg['action'] == 'authorized':
                print('Запуск GUI клиента')
                # app_a.start_chat_win()

            elif msg['action'] == 'registered':
                print('Запуск GUI клиента')
                # app_a.start_chat_win()

    def send_authorization_user(self, login, password):
        # self.authenticate_user()  # отправка собщения об аутенфикации
        print('Отправка формы авторизации', login, password)
        self.authenticate_user(password)

    def send_msg_to_user(self, data, login):
        """
        Отправка сообщения пользователю
        :param data: сообщение
        :param login: логин пользователя
        """
        msg = {
            'action': 'msg',
            'time': time.time(),
            'to': login,
            'from': self.name_client,
            'message': data
        }
        send_message(self.sock, msg)

    def authenticate_user(self, password):
        """
        Отправка сообщения об аутентификации
        """
        msg = {
            'action': 'presence',
            'login': self.name_client,
            'password': password
        }
        print('MMMSG', msg, self.sock)
        send_message(self.sock, msg)

    def get_all_users(self):
        """
        Запрос на получение списка всех юзеров
        """
        msg = {
            'action': 'get_users',
            'time': time.time()
        }
        send_message(self.sock, msg)

    def get_online_users(self):
        """
        Запрос на получение списка пользователей онлаин
        """
        msg = {
            'action': 'get_online_users',
            'time': time.time()
        }
        send_message(self.sock, msg)

    def get_contacts_list(self, user):
        """
        Получение списка контактов пользователя user
        :param user:
        """
        msg = {
            'action': 'get_contacts',
            'name': user,
            'time': time.time()
        }
        send_message(self.sock, msg)

    def add_user_in_contact(self, user):
        """
        запрос на добавление пользователя user в список контактов
        :param user:
        """
        # print('ghsjkdcsdc', user)
        msg = {
            'action': 'add_in_cotacts',
            'time': time.time(),
            'user': user
        }
        send_message(self.sock, msg)


if __name__ == '__main__':
    address = ParserSysArg(sys.argv)
    client_name = address.get_name()
    client_password = None

    print('Запуск GUI аторизации и регистрации')
    app = QtWidgets.QApplication(sys.argv)
    app_a = AuthUserWin()
    app_a.setWindowTitle('Авторизация')
    app.exec_()

    if not client_name or not client_password:
        client_name = app_a.login
        client_password = app_a.password_1
    else:
        exit(0)

    # создание базы данных
    print('Запуск базы данных')
    database = ClientDataBase(client_name)

    print('Запуск логики клиента')
    client = Client(
        database,
        address.get_address(),
        client_name,
        client_password,
        app_a.registration)
    client.daemon = True
    client.start()

    print('Запуск GUI чата')
    chat_app = ChatWin(database, client)
    chat_app.setWindowTitle(client_name)

    if client.authorisation:
        chat_app.show()
    else:
        error_app = ErrorWin(client.error_text)
        error_app.setWindowTitle('Error')
        error_app.show()

    app_a.close()
    sys.exit(app.exec_())
