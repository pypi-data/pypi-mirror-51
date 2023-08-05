import json
import sys
import re

from .settings import *
from descriptors.server_descriptor import *
print('ENCODING', ENCODING)


def dict_to_bytes(data_dict):
    """ Преобразование dict-объекта в байт-код """
    if isinstance(data_dict, dict):
        data = json.dumps(data_dict)
        return data.encode(ENCODING)
    else:
        raise TypeError


def bytes_to_dict(data_bytes):
    """ Преобразование байт-кода в dict-объект python """
    if isinstance(data_bytes, bytes):
        data = data_bytes.decode(ENCODING)
        return json.loads(data)
    else:
        raise TypeError


def send_message(sock, msg):
    """ Отправка сообщения """
    print('отправка сообщения в SEND MSG: ', msg)
    byte_message = dict_to_bytes(msg)
    sock.send(byte_message)


def receiving_message(sock):
    """ Получение сообщения """
    byte_message = sock.recv(1024)
    return bytes_to_dict(byte_message)


class ParserSysArg:
    """
    Парсингстроки
    """
    PORT = ValidNumberPort()

    def __init__(self, address):
        self.sys_arg_list = address
        self.IP = IP_SERVER_DEFAULT
        self.PORT = PORT_SERVER_DEFAULT
        self.setting_server_address()

    def setting_server_address(self):
        """
        установка IP-адреса и номера PORTа сервера
        :return:
        """
        print(self.sys_arg_list)
        if self.sys_arg_list:
            i = 1
            while True:
                if i >= len(self.sys_arg_list):
                    break

                if self.sys_arg_list[i] == '-a':
                    i += 1
                    pattern = re.compile(PATTERN_IP)
                    if re.match(pattern, self.sys_arg_list[i]):
                        self.IP = self.sys_arg_list[i]
                    else:
                        print(
                            'Переданный IP не валиден! Будет использован IP по умолчанию.')

                if self.sys_arg_list[i] == '-p':
                    i += 1
                    self.PORT = self.sys_arg_list[i]

                if self.sys_arg_list[i] == '-n':
                    i += 1
                    self.name = self.sys_arg_list[i]

                i += 1

    def get_address(self):
        return (self.IP, self.PORT)

    def get_name(self):
        try:
            self.name
        except AttributeError:
            pass
        else:
            return self.name
