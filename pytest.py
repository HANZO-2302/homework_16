from seminar_14_tests import dz_14

import pytest
from seminar_14_tests.dz_14 import *


@pytest.fixture
def data():
    return Company('Nike')

def test1(data):     #Проверка на наличие
    assert data.login('Евстафий Авдеевич Лихачев','610285')

def test2(data):     #Проверка на количнство символов ID
    with pytest.raises(Exception):
        assert data.login('Евстафий Авдеевич Лихачев','61025')

def test3(data):     #Проверка на возврат из login
    with pytest.raises(Exception):
        assert data.login('Евстафий Авдеевич Лихачев','61025')==('Евстафий Авдеевич Лихачев','61025',5)

def test4(data):
    with pytest.raises(LevelError):
        me=data.login('Никонова Ольга Андреевна','001114') #2
        n.hiring(me,'Ирина Хак','111211',3)  #если 1 то ошибка

if __name__ == '__main__':
    pytest.main(['-v'])