from socket import *
import json
from PyQt5 import QtWidgets
from select import select
from threading import Thread
import sys
import os
import re
import time
import hashlib
import hmac
import binascii

from gui_server.main import *
# from .gui_server.main import *

from jim.settings import *
from jim.utils import *
from metaclasses.server_meta import *
from db.server_db import *


class Server(Thread, metaclass=ServerMeta):
    """
    Класс сервера
    """

    def __init__(self, database):
        address = ParserSysArg(sys.argv)
        self.address = address.get_address()
        self.clients = {}
        self.server = database
        super().__init__()

    def run(self):
        """
        Запуск сервера
        :return:
        """
        print(self.server.get_users_list())
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(self.address)
        self.sock.listen(5)
        self.sock.settimeout(0.5)
        self.make_connection()

    def make_connection(self):
        print('start_server')
        while True:
            try:
                client, addr = self.sock.accept()
            except OSError:
                pass
            else:
                print(client, '-=-', self.clients)
                if client not in self.clients.keys():
                    self.first_connection(client, 'ip')
                # self.clients[client] = msg['login']
            finally:
                r = []
                w = []
                try:
                    r, w, e = select(
                        self.clients.keys(), self.clients.keys(), [])
                    # r, w, e = select(client, client, [])
                except BaseException:
                    pass
                requests = self.get_responses(r)
                print('requests', requests)
                self.write_responses(requests, w)
        self.sock.close()

    def registration_user(self, requests, sock_client, ip):
        if requests['login'] in self.server.get_login_users_list():
            msg = {
                'response': 400,
                'alert': 'Клиент с таким логином уже существует'
            }
            send_message(sock_client, msg)

        passwd_bytes = requests['password'].encode('utf-8')
        salt = requests['login'].lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        self.server.log_in(
            requests['login'],
            binascii.hexlify(passwd_hash),
            ip)
        msg = {
            'response': 511,
            'login': requests['login']
        }
        self.clients[sock_client] = requests['login']
        send_message(sock_client, msg)

    def first_connection(self, sock, ip):
        requests = receiving_message(sock)
        print(
            'Список зарегестрированных пользователей',
            self.server.get_users_list())
        print(
            'Список пользователей онлаин',
            self.server.get_login_users_list())
        print('Имя подключаемого клиента  ', requests['login'])
        print('Сообщение от клиента  ', requests)
        if requests['action'] == 'registration':
            self.registration_user(requests, sock, 'ip')
            return
        if requests['action'] == 'authorization':
            self.authorization_user(requests, sock, 'ip')
            return

    def authorization_user(self, requests, sock_client, ip):
        if requests['login'] in self.server.get_login_users_list():
            random_str = binascii.hexlify(os.urandom(64))
            data = random_str.decode('ascii')
            hash = hmac.new(
                self.server.get_pass_user(
                    requests['login']),
                random_str)
            digest = hash.digest()
            msg = {
                'response': 500,
                'data': data
            }
            try:
                send_message(sock_client, msg)
                answer = receiving_message(sock_client)
                client_digest = binascii.a2b_base64(answer['data'])
            except OSError:
                pass

            if hmac.compare_digest(digest, client_digest):
                self.clients[sock_client] = answer['login']
                print('Сохраняем в словаре', self.clients)
                msg = {
                    'response': '511',
                    'login': requests['login']
                }
                print('Отправление сообщения об успешной авторизации')
                send_message(sock_client, msg)
                self.server.add_user_in_online_table(answer['login'])
            else:
                msg = {
                    'response': '400',
                    'alert': 'Введенный пароль не верен'
                }
                send_message(sock_client, msg)
        else:
            msg = {
                'response': '400',
                'alert': 'Клиент с таким логином не зарегистрирован'
            }
            send_message(sock_client, msg)
        return

    def formation_response_message(self, msg):
        """
        Формирование ответа клиенту
        :param msg: словарь type(dict)
        :return: словарь type(dict)
        """
        print('MSG', msg)
        if 'action' in msg and \
                'time' in msg and \
                isinstance(msg['action'], str) and \
                len(msg['action']) <= 15 and \
                isinstance(msg['time'], float):

            return {
                'response': 200,
                'time': time.time(),
                'alert': ERROR_LIST['200']
            }
        else:
            return {
                'response': 400,
                'time': time.time(),
                'alert': ERROR_LIST['400']
            }

    def get_responses(self, read_clients):
        responses = {}
        print('read_clients', read_clients)
        for sock_client in read_clients:
            try:
                msg = receiving_message(sock_client)
                print('Получено сообщение', msg)
                responses[sock_client] = msg
            except BaseException:
                # pass
                self.clients.pop(sock_client)
        print('responses', responses)
        return responses

    def write_responses(self, requests, write_clients):
        for sock_client in write_clients:
            for key in requests:
                try:
                    print('TRRRRRYYYYY ', requests[key])
                    if (requests[key]['action'] == 'msg'
                        or requests[key]['action'] == 'message') \
                        and requests[key] \
                        and sock_client != key\
                        and (requests[key]['to'] == self.clients[sock_client]
                             or requests[key]['to'] == '#all'):
                        self.server.message_to_client(
                            requests[key]['from'], requests[key]['to'])
                        send_message(sock_client, requests[key])

                    # подключение пользователя
                    elif requests[key]['action'] == 'presence':
                        print(
                            'Список зарегестрированных пользователей',
                            self.server.get_users_list())
                        if (requests[key]['login'] ==
                                self.clients[sock_client]):
                            self.first_connection(
                                requests[key], sock_client, 'ip')

                    elif requests[key]['action'] == 'registration':
                        print(
                            'Список зарегестрированных пользователей',
                            self.server.get_users_list())
                        if (requests[key]['login'] ==
                                self.clients[sock_client]):
                            self.registration_user(
                                requests[key], sock_client, 'ip')

                    elif requests[key]['action'] == 'get_users':
                        msg = {
                            'response': 202,
                            'action': 'users_list',
                            'data': self.server.get_login_users_list()
                        }
                        print(msg)
                        send_message(sock_client, msg)

                    elif requests[key]['action'] == 'get_online_users':
                        msg = {
                            'response': 202,
                            'action': 'online_users_list',
                            'data': self.server.get_login_users_list()
                        }
                        print(msg)
                        send_message(sock_client, msg)

                    elif requests[key]['action'] == 'add_contact' and \
                            requests[key]['user_login'] == self.clients[sock_client]:
                        print()
                        msg = {
                            'response': self.server.add_contact(
                                requests[key]['user_login'],
                                requests[key]['nickname'])}
                        send_message(sock_client, msg)

                    elif requests[key]['action'] == 'add_in_cotacts':
                        print(
                            f'Мой логин {self.clients[sock_client]}, добавляемый контакт {requests[key]["user"]}')
                        self.server.add_contact(
                            self.clients[sock_client], requests[key]['user'])
                        # print("Список всех контактов из БД", self.server.get_contact_users_list(self.clients[sock_client]['name']))

                    elif requests[key]['action'] == 'get_contacts':
                        print(
                            'dsfgggggggggGGGGGGGGGGGGGjjjjjjj ',
                            requests[key])
                        msg = {
                            'action': 'contacts_list',
                            'data': self.server.get_contact_users_list(
                                requests[key])}
                        send_message(sock_client, msg)

                    elif requests[key]['action'] == 'del_contact' and \
                            requests[key]['user_login'] == self.clients[sock_client]:
                        msg = {
                            'response': self.server.del_contact(
                                requests[key]['user_login'],
                                requests[key]['nickname'])}
                        send_message(sock_client, msg)
                except BaseException:
                    sock_client.close()
                    self.clients.pop(sock_client)


def main():
    database = ServerDataBase()

    s = Server(database)
    s.daemon = True
    s.start()

    app = QtWidgets.QApplication(sys.argv)
    users_list_app = UsersListWin(database)
    users_list_app.setWindowTitle('Users list')
    users_list_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
