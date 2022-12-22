from data import db_session
from data.users import Users
from data.product import Product

from tabulate import tabulate

#Подключение бд
db_session.global_init("data/magazine_db.db")
db_sess = db_session.create_session()


class User:

    def __init__(self, id, name, password, role):
        """
        Заполнение параметров по умолчанию
        :param id: айди юзера
        :param name: имя
        :param password: пароль
        :param role: роль
        """
        self.id_use = int(id)
        self.name = name
        self.password = password
        self.role = int(role)

    def products(self):
        """
        Выводит товары со склада
        :return:
        """
        prods = db_sess.query(Product)
        headers = []
        haracteristics = []

        for i in prods:
            head = []
            har = []
            for j in i.to_dict().keys():
                head.append(j)
                har.append(i.to_dict()[j])

            headers = head
            haracteristics.append(har)

        print(tabulate(haracteristics, headers=headers))

    def change_password(self):
        """
        Меняет паароль пользователя
        :return:
        """
        new_pass = input("Введите новый пароль: ")
        db_sess.query(Users).filter(Users.id == self.id_use).update(
            {Users.password: new_pass}, synchronize_session=False
        )
        db_sess.commit()
        print("Готово")
        print()


class Admin(User):

    def add_product(self):
        """
        Добавляет новый товар в ьд
        :return:
        """
        try:
            new_prod = Product()
            new_prod.name = input("ведите название нового продукта: ")
            new_prod.description = input("Введите описание нового продукта: ")
            new_prod.postav = input("Введите поставщика: ")
            new_prod.price = int(input("Введите цену продукта: "))
            new_prod.count = int(input("Введите количество продукта на складе: "))

            db_sess.add(new_prod)
            db_sess.commit()
            db_sess.rollback()

        except (Exception):
            print("Что-то пошло не так")

    def delete(self, id):
        """
        Удаление товара по айди
        :param id: айди товара
        :return:
        """
        try:

            db_sess.query(Product).filter(Product.id == id).delete(synchronize_session=False)
            db_sess.commit()
            print("Готово")

        except (Exception):
            print("Что-то пошло не так")

    def change_somthing_product(self, id):
        """
        Меняет выбранный пользователем атрибут
        :param id: айди товара который нужно поменять
        :return:
        """
        try:
            atribute = input("Введите атрибут который хотите поменять у товара: ")
            #Проверка на автрибут замены введённый юзером
            if atribute == "description":
                new = input("Введите новое описание: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.description: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Готово")

            elif atribute == "postav":
                new = input("Введите нового поставщика: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.postav: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Готово")

            elif atribute == "count":
                new = int(input("Введите новое количество: "))
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.count: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Готово")

            elif atribute == "price":
                new = int(input("Введите новую цену: "))
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.price: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Готово")

            elif atribute == "name":
                new = input("Введите новое название: ")
                db_sess.query(Product).filter(Product.id == id).update(
                    {Product.name: new}, synchronize_session=False
                )
                db_sess.commit()
                print("Готово")

            else:
                print("Такого атрибута нет")


        except (Exception):
            print("Похоже такого товара нету на складе")


def autorize():
    """
    Авторизация пользователя
    :return: в случае удачной регистрации - возвращает кортеж (экз. класса, 1)
    """
    name = input("Введите имя: ")
    password = input("Введите пароль: ")
    re_passw = input("Повторите пароль: ")

    if password == re_passw:
        try:

            user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()
        #Проверки на удачную авторизацию
            if user:
                print('hh')
                return (user, 1)

            else:
                return (0, 0)

        except (Exception):
            return (0, 0)

    else:
        return (0, 0)


def reg():
    """
    Решистрирут пользователя, если пользователь с введённым именем существует,
     то он должен авторизоваться подним
    :return:
    """
    name = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    try:
        #Проверка на ниличие пользователя в бд
        user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()
        if str(user.name) == name:
            print("Такой пользователь уже существует, авторизуйтесь под ним")
            return autorize()

    except (Exception):
        #Добавление нового пользователя
        new_user = Users()
        new_user.name = name
        new_user.password = password
        new_user.role = 0

        db_sess.add(new_user)
        db_sess.commit()
        db_sess.rollback()

        return (new_user, 1)


def interface_admin(adm):
    """
    Выводит интерфейс для админа с его основным функционалом
    :param adm: экземпляр класса админ
    :return:
    """
    while (True):
        #Вывод товаров со склада
        adm.products()
        print()
        print("Введите что хотите сделать: 1 - редактировать, 2 - удалить, 3 - добавить: ")
        inp = int(input("Введите: "))
        try:
            #Изменение одного из параметров товара, на выбор
            if inp == 1:
                id_of_prod = int(input("Введите ID товара который хотите изменить: "))
                adm.change_somthing_product(id_of_prod)

            #Удаление товара
            elif inp == 2:
                id_of_prod = int(input("Введите ID товара который хотите изменить: "))
                adm.delete(id_of_prod)

            #Добавление нового товара
            elif inp == 3:
                adm.add_product()

            else:
                print("Такого нету")
        #Исключение на рандомные ошибки
        except (Exception):
            print("Похоже вы ввели не верный код")


def interface_for_user(use):
    """
    Спавнит интерфейс для юзера, с его функционалом
    :param use: экземпляр класса юзер
    :return:
    """
    while (True):
        #Вывод товарор со склада
        use.products()
        print()
        print("Введите что хотите сделать: 1 - изменить пароль: ")
        inp = int(input("Введите: "))
        try:
            #Смена пароля
            if inp == 1:
                use.change_password()
                print("nice")
                print()

            else:
                print("Такого нету")
                print()

        #Вывод кода ошибки
        except (Exception) as e:
            print(e)
            print()


def main():
    """
    Проверят под каким пользователем зашёл юзер, или зарегистрировался
    :return:
    """
    print("Что вы хотите сделать: 1 - авторизоваться, 2 - зарегистрироваться")
    inp = int(input())
    if inp == 1:
        res_aut = autorize()
        #Проверка на пользователя
        if res_aut[1] == 1:
            if res_aut[0].role == 0:
                user = User(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
                interface_for_user(user)
            elif res_aut[0].role == 1:
                admin = Admin(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
                interface_admin(admin)

        else:
            print("Переделывай")

    elif inp == 2:
        res_reg = reg()
        #Проверка на пользователя
        if res_reg[1] == 1:
            if res_reg[0].role == 0:
                user = User(res_reg[0].id, res_reg[0].name, res_reg[0].password, res_reg[0].role)
                interface_for_user(user)
            elif res_reg[0].role == 0:
                admin = Admin(res_reg[0].id, res_reg[0].name, res_reg[0].password, res_reg[0].role)
                interface_admin(admin)

        else:
            print("Переделывай")


if __name__ == "__main__":
    main()