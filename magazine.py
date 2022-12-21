from data import db_session
from data.users import Users
from data.product import Product

from tabulate import tabulate

db_session.global_init("data/magazine_db.db")
db_sess = db_session.create_session()


class User:
    def __init__(self, id, name, password, role):
        self.id = id
        self.name = name
        self.password = password
        self.role = role

    def change_password(self):
        new_pass = input("Введите новый пароль: ")
        db_sess.query(User).filter(Users.id == self.id).update(
            {Users.password: new_pass}, synchronize_session=False
        )
        db_sess.commit()

class Admin(User):
    def products(self):
        prods = db_sess.query(Product)
        headers = []
        haracteristics = []

        for i in prods:
            head = []
            har = []
            for j in i.to_dict().keys():
                head.append(j)
                har.append(i[j])

            headers = head
            haracteristics.append(har)

        print(tabulate(haracteristics, headers=headers))

    def Add_User(self):
        new_prod = Product()
        new_prod.name = input()
        new_prod.description = input()
        new_prod.postav = input()
        new_prod.price =  int(input())
        new_prod.count =  int(input())

        db_sess.add(new_prod)
        db_sess.commit()
        db_sess.rollback()
    def delete(self, id):
        db_sess.query(Product).filter(Product.id == id).delete(synchronize_session=False)
        db_sess.commit()
        print("Готово")
    def change_somthing_product(self, id):
        try:
            prod = db_sess.query(Product).filter(Product.id == id).one()
            atribute = input("Введите атрибут который хотите поменять у товара: ")

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
    name = input()
    password = input()
    re_passw = input()

    if password == re_passw:
        try:

            user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()

            if user:
                return (user, 1)

            else:
                return (0, 0)

        except (Exception):
            return (0, 0)

    else:
        return (0, 0)


def interface_admin(adm):
    while (True):
        adm.products()
        print()
        print("Введите что хотите сделать: 1 - редактировать, 2 - удалить, 3 - добавить: ")
        inp = int(input("Введите: "))
        try:
            if inp == 1:
                id_of_prod = int(input("Введите ID товара который хотите изменить: "))
                adm.change_somthing_product(id_of_prod)

            elif inp == 2:
                id_of_prod = int(input("Введите ID товара который хотите изменить: "))
                adm.delete(id_of_prod)

            elif inp == 3:
                adm.Add_User()

            else:
                print("Такого нету")

        except (Exception):
            print("Похоже вы ввели не верный код")


def main():
    res_aut = autorize()
    if res_aut[1] == 1:
        if res_aut[0].role == 0:
            user = User(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
        elif res_aut[0].role == 0:
            admin = Admin(res_aut[0].id, res_aut[0].name, res_aut[0].password, res_aut[0].role)
            interface_admin(admin)

    else:
        print("Переделывай")


if __name__ == "__main__":
    main()