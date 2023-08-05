class ValidNumberPort:
    def __get__(self, instance, owner):
        return instance.__dict__[self.my_attr]

    def __set__(self, instance, value):
        try:
            int(value)
        except ValueError:
            print('Введен недопустимый номер порта! Будет использован порт по умолчанию.')
        except:
            pass
        else:
            if 1023 < int(value) <= 65535:
                instance.__dict__[self.my_attr] = int(value)
            else:
                raise ValueError('Номер порта должен лежать в диапазоне: 1023-65535')

    def __set_name__(self, owner, my_attr):
        self.my_attr = my_attr
