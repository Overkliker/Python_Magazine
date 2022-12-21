from data import db_session
from data.users import Users
from data.product import Product

db_session.global_init("data/magazine_db.db")
db_sess = db_session.create_session()


class User:
    def __init__(self, id, name, password, role):
        self.id = id
        self.name = name
        self.password = password
        self.role = role

    def change_password(self,):
        new_pass = input("Введите новый пароль: ")
        db_sess.query(User).filter(Users.id == self.id).update(
            {Users.password: new_pass}, synchronize_session=False
        )
        db_sess.commit()

class Admin(User):
    pass

def autorize():
    name = input()
    password = input()
    re_passw = input()

    if password == re_passw:
        try:

            user = db_sess.query(Users).filter(Users.password == password).one()

            if user:
                return (user, 1)

            else:
                return (0, 0)

        except (Exception):
            return (0, 0)

    else:
        return (0, 0)


def interface_admin(adm):
    pass


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