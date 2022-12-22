from data import db_session
from data.users import Users
from data.product import Product
from tabulate import tabulate

db_session.global_init("data/magazine_db.db")
db_sess = db_session.create_session()

prods = db_sess.query(Product)
headers = []
haracteristics = []

for i in prods:
    head = []
    har = []
    for j in i.to_dict().keys():
        print(i)
        head.append(j)
        har.append(i.to_dict()[j])

    headers = head
    haracteristics.append(har)

print(tabulate(haracteristics, headers=headers))

