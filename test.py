from data import db_session
from data.users import Users
from data.product import Product
from tabulate import tabulate

db_session.global_init("data/magazine_db.db")
db_sess = db_session.create_session()

name = 'gg'
password = '123'
user = db_sess.query(Users).filter(Users.password == password and Users.name == name).one()
print(user.id)