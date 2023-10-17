import json
import os
import random
from faker import Faker

def create_employee(company:str, count:int):
    employees={}
    list_id=[]
    for _ in range(count):
        name=Faker('ru_RU').name()
        while True:
            employee_id=str(random.randint(1,999999)).zfill(6) #заполняется до 6-ти значного числа
            if employee_id not in list_id:
                list_id.append(employee_id)
                break
        lvl_access=int(employee_id)%7+1
        if lvl_access in employees:
            employees[lvl_access][employee_id]=name
        else:
            employees[lvl_access]={employee_id: name}
    with open(f'{company}.json', 'w', encoding='UTF-8') as file:
        json.dump(employees,file,indent=4,ensure_ascii=False)
    return employees

#create_employee('adidas',10)

#создаем дискрипторы
class EmployeeName:
    def __set_name__(self,owner,name):
        self.parameter_name='_' + name

    def __get__(self,instance,owner):
        return getattr(instance,self.parameter_name)

    def __set__(self,instance,value:str):
        if not all([all(list(map(lambda x: x.isalpha(), name))) for name in value.split()]):
            raise ValueError(f'Имя может состоять только из букв: {value}')
        if not all(map(lambda x: x.istitle(), value.split())):
            raise ValueError(f'Имена должны быть с большой буквы: {value}')
        setattr(instance,self.parameter_name,value)

#дискриптор
class EmployeeID:
    def __set_name__(self,owner,name):
        self.parameter_name='_' + name

    def __get__(self,instance,owner):
        return getattr(instance,self.parameter_name)

    def __set__(self,instance,value:str):
        if not len(value)==6:
            raise ValueError(f'ID должен быть шестизначным: {value}')
        if not value.isdigit():
            raise ValueError(f'ID должен содержвть только цифры: {value}')
        setattr(instance,self.parameter_name,value)


class Emploee:
    name=EmployeeName
    employee_id=EmployeeID

    def __init__(self,name,lvl_access:int,employee_if:str):
        self.name=name
        self.employee_id=employee_if
        if 0<int(lvl_access)<8:
            self.lvl_access=int(lvl_access)
        else:
            raise ValueError

    def __str__(self):
        return f'{self.name} ({self.employee_id}) | Доступ: {self.lvl_access}'

    def __eq__(self, other:str):
        return self.name==other.name and self.employee_id==other.employee_id

# me=Emploee('Елена',7,'456456')
# print(me)

#Excaple - проверки на ошибки
class OwnBasicException(Exception):
    def __init__(self, message:str):
        self.massage=message

    def __str__(self):
        return f'{self.massage}'

class LevelError(OwnBasicException):
    def __init__(self, me,new):
        super(LevelError,self).__init__(f'Ошибка доступа! Служащий ({me.name}, доступ: {me.lvl_access})'
                                        f'не имеет права создать служащего ({new.name}, доступ: {new.lvl_access})'
                                        f'выше собственного уровня доступа')

    def __str__(self):
        return f'{self.massage}'




class Company:
    def __init__(self,name) -> None:
        self.name=name
        if os.path.exists(f'{self.name}.json'): #если  файл  нет
            with open(f'{self.name}.json', 'r', encoding='UTF-8') as file:
                emploees_list=json.load(file)
        else:
            emploees_list=create_employee(self.name,10)
        self.employes=[Emploee(e_name,e_lvl,e_id)
                       for e_lvl,person in emploees_list.items()
                       for e_id,e_name in person.items()] #собираем список объектов




    def login(self,name,e_id):
        for employee in self.employes:
            if employee.name==name and employee.employee_id==e_id:
                return employee
        return False



    def hiring(self,me:Emploee,new_name:str,new_id:str, new_lvl:int):
        if me:
            if me.lvl_access>new_lvl:
                if new_id not in [employee.employee_id for employee in self.employes]: #собираем список ID
                    self.employes.append(Emploee(new_name,int(new_lvl),new_id))
                    self.__save()
                else:
                    print('Такой ID уже есть')
            else:
                raise LevelError(me,Emploee(new_name,new_lvl,new_id))
        else:
            print('Ошибка доступа')

    def __save(self):
        employees_list={}
        for employee in self.employes:
            if employee.lvl_access in employees_list:
                employees_list[employee.lvl_access]={employee.employee_id: employee.name} #если есть уровень
            else:
                employees_list[employee.lvl_access]={employee.employee_id:employee.name} #если нет уровня
        with open(f'{self.name}.json','w', encoding='UTF-8') as file:
            json.dump(employees_list,file,indent=4,ensure_ascii=False)



n=Company('Nike')
me = n.login('Рожкова Вероника Матвеевна','001114')
n.hiring(me,'Марк Вячеславович Комаров','855301',1)