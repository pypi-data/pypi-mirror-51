import dis
from pprint import pprint


class ServerMeta(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attributs = []
        for key, value in clsdict.items():
            if key.startswith("__"): continue

            for i in dis.get_instructions(clsdict[key]):
                if i.opname == 'LOAD_GLOBAL':
                    if i.argval not in attributs:
                        attributs.append(i.argval)
                if i.opname == 'LOAD_ATTR':
                    if i.argval not in methods:
                        methods.append(i.argval)

        # print(methods)
        if 'connect' in methods:
            raise TypeError('Метод connect в классе сервера недопустим')
        if 'AF_INET' not in attributs or 'SOCK_STREAM' not in attributs:
            raise TypeError('Для работы по TCP при создании сокета необходимо передать параметры AF_INET и SOCK_STREAM')
        type.__init__(self, clsname, bases, clsdict)