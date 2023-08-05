from db.client_db import ClientDataBase
from jim.utils import ParserSysArg
from jim.settings import *
from gui import chat_window, add_users, authorization, auth, error
import client
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import re
import time
from threading import Thread

from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))


class ErrorWin(QtWidgets.QMainWindow):
    """
    Класс - окно вывода аврийных сообений
    """

    def __init__(self, data, parent=None):
        # super.__init__(self, parent)
        QtWidgets.QWidget.__init__(self, parent)
        self.error_ui = error.Ui_MainWindow()
        self.error_ui.setupUi(self)
        # self.error_ui.textEdit.setText(data)
        self.error_ui.textBrowser.setText(data)
        self.show()


class AuthUserWin(QtWidgets.QMainWindow):
    """
    Класс - окно авторизации и регистрации
    """

    def __init__(self, parent=None):
        # super.__init__(self, parent)
        QtWidgets.QWidget.__init__(self, parent)
        self.auth_ui = authorization.Ui_MainWindow()
        self.auth_ui.setupUi(self)

        self.auth_ui.label_4.hide()
        self.auth_ui.label_5.hide()
        self.auth_ui.textBrowser_3.hide()
        self.auth_ui.pushButton_3.hide()

        self.login = None
        self.password_1 = None
        self.password_2 = None
        self.registration = False
        self.auth_ui.textBrowser.setReadOnly(False)
        self.auth_ui.textBrowser_2.setReadOnly(False)
        self.auth_ui.textBrowser_3.setReadOnly(False)
        self.auth_ui.pushButton.clicked.connect(self.authorization_user)
        self.auth_ui.pushButton_2.clicked.connect(self.registration_user)

        self.show()

    def authorization_user(self):
        """
        Обработчик кнопки "Вход"
        """
        self.auth_ui.pushButton.clicked.connect(lambda: self.validate(False))

    def registration_user(self):
        """
        Обработчик кнопки "Регистрация"
        """
        self.registration = True
        self.auth_ui.label_4.show()
        self.auth_ui.label_5.show()
        self.auth_ui.textBrowser_3.show()
        self.auth_ui.pushButton_3.show()
        self.auth_ui.label.hide()
        self.auth_ui.pushButton.hide()
        self.auth_ui.pushButton_2.hide()
        self.auth_ui.pushButton_3.clicked.connect(lambda: self.validate(True))

    def validate(self, type_valid):
        """
        Проверка правильности введенных данных
        """
        if type_valid:
            self.login = self.auth_ui.textBrowser.toPlainText()
            self.password_1 = self.auth_ui.textBrowser_2.toPlainText()
            self.password_2 = self.auth_ui.textBrowser_3.toPlainText()
        else:
            self.login = self.auth_ui.textBrowser.toPlainText()
            self.password_1 = self.auth_ui.textBrowser_2.toPlainText()

        if type_valid and \
                self.login and \
                self.password_1 and \
                self.password_2 and \
                self.password_1 == self.password_2:
            print(
                'Логин',
                self.login,
                'Пароль-1',
                self.password_1,
                'Пароль-2',
                self.password_2)
            QtWidgets.qApp.exit()
        elif not type_valid and self.login and self.password_1:
            print('Логин', self.login, 'Пароль-1', self.password_1)
            QtWidgets.qApp.exit()

        if not self.login:
            self.auth_ui.label_2.setStyleSheet("QLabel { color: red; }")
        else:
            self.auth_ui.label_2.setStyleSheet("QLabel { color: black; }")

        if not self.password_1:
            self.auth_ui.label_3.setStyleSheet("QLabel { color: red; }")
        else:
            self.auth_ui.label_3.setStyleSheet("QLabel { color: black; }")
        if type_valid and not self.password_2:
            self.auth_ui.label_5.setStyleSheet("QLabel { color: red; }")
        else:
            self.auth_ui.label_5.setStyleSheet("QLabel { color: black; }")
        if type_valid and self.password_1 != self.password_2:
            self.auth_ui.label_5.setText(
                'Повторите пароль (ПАРОЛИ НЕ СОВПАДАЮТ)')
            self.auth_ui.label_5.setStyleSheet("QLabel { color: red; }")
        else:
            self.auth_ui.label_5.setText('Повторите пароль')
            self.auth_ui.label_5.setStyleSheet("QLabel { color: red; }")


class ChatWin(QtWidgets.QMainWindow):
    """
    Класс - основное окно чата
    """

    def __init__(self, db, client, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.db = db
        self.client = client

        self.ui = chat_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textBrowser.setReadOnly(True)

        self.model = QtGui.QStandardItemModel()
        self.model_chat = QtGui.QStandardItemModel()
        self.add_user = AddUsersWin(self.db, self.client, self)
        self.installing_handlers()

    def installing_handlers(self):
        """
        Инициализация окна чата
        """
        time.sleep(0.1)
        # отображение списка контактов
        self.contacts_to_display()
        # обработчик при выборе собеседника из списка контактов
        self.ui.listView.clicked.connect(self.event_contact_selected)
        # обработчик кнопки "Удалить контакт"
        self.ui.pushButton.clicked.connect(self.del_contact)
        # обработчик кнопки "Добавить контакт"
        self.ui.pushButton_2.clicked.connect(self.add_user_in_contacts_list)
        # обработчик кнопки "Отправить сообщение"
        self.ui.pushButton_3.clicked.connect(self.send_message)

    def contacts_to_display(self):
        """
        Отображение списка контактов
        """
        self.model.clear()
        # получение списка контактов из локальной БД
        users_list = self.db.get_contact_list()
        for user in users_list:
            item = QtGui.QStandardItem(user.user_name)
            item.setBackground(QtGui.QColor(230, 230, 250))
            self.model.appendRow(item)
        self.ui.listView.setModel(self.model)

    def event_contact_selected(self):
        """
        Событие наступающее при выборе пользователя из списка контактов.
        """
        obj = self.ui.listView.selectedIndexes(
        )[0]                 # Получение выбранного объекта-пользователя
        # Позиция выбранного пользователя
        self.numb = obj.row()
        # Логин выбранного полльзователя
        self.value = obj.data()
        if self.value:
            self.msg_list = self.db.get_message_user(
                self.value)    # Получение истории сообщений
            self.model_chat.clear()                                 # Очистка окна чата
            # Отображение истории сообщений в окне чата
            self.display_chat_messages()
            # Разблокировка окна ввода сообщений
            self.ui.textBrowser.setReadOnly(False)
            element = self.model.findItems(self.value)
            element[0].setBackground(QtGui.QColor(230, 230, 250))
        else:
            # Блокировка окна ввода сообщений
            self.ui.textBrowser.setReadOnly(True)

    def add_contact(self, user):
        """
        добавление пользователя в список контактов
        :param user: логин пользователя
        """
        self.client.add_user_in_contact(
            user)               # добавление пользователя в контакты
        # добавление пользователя в окно с контактами
        self.model.appendRow(QtGui.QStandardItem(user))

    def del_contact(self, number=None):
        """
        Удаление контакта по номеру его позиции в списке контактов
        :param number: число
        """
        try:
            if not number:
                self.model.removeRow(self.numb)
                self.db.del_contact(self.value)
                self.model_chat.clear()
                self.ui.textBrowser.setReadOnly(True)
            else:
                self.model.removeRow(number)
        except BaseException:
            pass

    def add_user_in_contacts_list(self):
        """
        Запуск окна добавления пользователя в контакты
        """
        self.client.get_online_users()
        self.add_user.setWindowTitle('List users')
        self.add_user.show()

    def send_message(self):
        """
        Получение введенного сообщения и отправка его пользователю
        """
        msg = self.ui.textBrowser.toPlainText()  # Получение текста введенного сообщения
        self.client.send_msg_to_user(msg, self.value)
        # Добавление сообщения в локальную БД
        self.db.send_message(msg, True, self.value)
        self.add_msg_in_display_chat(
            msg, True, self.value)  # Вывод сообщения в чат
        self.ui.textBrowser.clear()  # Очистка окна ввода сообщений

    def display_chat_messages(self, user=None):
        """
        Вывод сообщений чата выбранного контакта
        """
        if isinstance(self.msg_list, list):
            for el in self.msg_list:
                item = QtGui.QStandardItem(el.msg)
                if el.message_type:
                    item.setTextAlignment(Qt.AlignRight)
                    item.setBackground(QtGui.QColor(250, 128, 114))
                else:
                    item.setTextAlignment(Qt.AlignLeft)
                    item.setBackground(QtGui.QColor(152, 251, 152))
                self.model_chat.appendRow(item)
            self.ui.listView_2.setModel(self.model_chat)
        # автопрокрутка вниз истории сообщений
        self.ui.listView_2.scrollToBottom()

    def add_msg_in_display_chat(self, msg, type_msg, user):
        """
        Добавление сообщения в текущий чат
        :param msg: str сообщение
        :param type_msg: True - сообщение получено, False - отправленное сообщение
        :param user: логин собеседника
        """
        try:
            # если выбран хотяб один из контактов
            if user == self.value:
                # вывод истории сообщений с текущим пользователем
                self.event_contact_selected()
            else:
                # если пользователь есть в контактах но его чат не активен,
                # получаем его объект
                element = self.model.findItems(user)
                if element:
                    # выделяем пользователя зеленым цветом
                    element[0].setBackground(QtGui.QColor(0, 255, 0))
                else:
                    # если нет отправлям запрос серверу на добавление в
                    # контакты
                    self.add_contact(user)
                    # находим пользователя и красим его в зеленый
                    element = self.model.findItems(user)[0]
                element.setBackground(QtGui.QColor(0, 255, 0))
        except AttributeError:
            element = self.model.findItems(user)
            if element:
                element[0].setBackground(QtGui.QColor(0, 255, 0))
            else:
                self.add_contact(user)
                element = self.model.findItems(user)
            element[0].setBackground(QtGui.QColor(0, 255, 0))


class AddUsersWin(QtWidgets.QMainWindow):
    """
    Класс - окно добавления пользователя в список контактов
    """

    def __init__(self, db, client, chat_win, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.db = db
        self.client = client
        self.chat_win = chat_win

        self.addUserWin = add_users.Ui_MainWindow()
        self.addUserWin.setupUi(self)

        self.buttonAddInContacts()

    def buttonAddInContacts(self):
        """
        Установка обработчика на кнопку добавить пользователя в контакты
        """
        self.addUserWin.pushButton.clicked.connect(self.add_user_in_contact)

    def display_users_list(self, lst):
        """
        Выводит списка доступных контактов в меню добавления контактов
        :param lst: list список контактов
        """
        if self.client.name_client in lst:
            lst.remove(self.client.name_client)
        self.addUserWin.comboBox.clear()
        # отображение списка контактов в выпадающем меню
        self.addUserWin.comboBox.addItems(lst)

    def add_user_in_contact(self):
        """
        Добавление пользователя в БД и в окно с контактами
        :return:
        """
        name = self.addUserWin.comboBox.currentText(
        )   # получение логина из текстового поля
        # добавление записи в базу и в окно с контактами
        self.chat_win.add_contact(name)
