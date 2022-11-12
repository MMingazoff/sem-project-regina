import random
import psycopg2


class DataBase:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname='regina',
            user='postgres',
            password='marat2003',
            host='localhost',
            port='5432'
        )
        self.con.autocommit = True
        self.cur = self.con.cursor()

    def get_user_by_id(self, user_id):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.cur.fetchone()
            return res
        except Exception as exc:
            print(str(exc))
            return False

    def register_user(self, first_name, last_name, email, phone_num, password):
        try:
            self.cur.execute(
                "INSERT INTO users (first_name, last_name, email, phone_num, password) VALUES (%s, %s, %s, %s, %s)",
                (first_name, last_name, email, phone_num, password))
        except Exception as e:
            print(e)

    def check_user_email_phone(self, email, phone):
        try:
            self.cur.execute("SELECT * FROM users WHERE email = '%s' or phone_num = '%s'" % (email, phone))
            if not self.cur.fetchone():
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_by_email(self, email):
        try:
            self.cur.execute("SELECT * FROM users WHERE email = '%s'" % email)
            res = self.cur.fetchone()
            if not res:
                return False
            return res
        except Exception as e:
            print(e)
            return False

    def get_all_product(self):
        try:
            self.cur.execute("SELECT * FROM products")
            res = self.cur.fetchall()
            return res
        except Exception as e:
            print(e)
            return False

    def get_product_by_id(self, id):
        try:
            self.cur.execute("SELECT * FROM products WHERE id = '%s'" % id)
            res = self.cur.fetchone()
            if not res:
                return False
            return res

        except Exception as e:
            print(e)
            return False

    def delete_product_by_id(self, id):
        try:
            self.cur.execute("DELETE FROM products WHERE id = '%s'" % id)
        except Exception as e:
            print(e)
            return False

    def get_all_orders(self, user_id):
        try:
            self.cur.execute("SELECT * FROM orders WHERE user_id = %s" % user_id)
            orders = self.cur.fetchall()
            res = []
            for create_date, total, _, id in orders:
                self.cur.execute(
                    "SELECT title, amount, cost, image_url, id FROM products JOIN "
                    "(SELECT product_id, order_id, count(*) amount "
                    "FROM purchases GROUP BY product_id, order_id) p ON p.product_id = products.id "
                    "WHERE order_id = %s" % id
                )
                products = self.cur.fetchall()
                res.append(tuple((id, create_date, total, products)))
            return res
        except Exception as e:
            print(e)
            return False

    def create_order(self, user_id):
        # TODO('сделать id serial')
        products, total = self.get_cart_with_total(user_id)
        self.cur.execute("SELECT id FROM orders ORDER BY id DESC")
        last_id = self.cur.fetchone()[0]
        self.cur.execute("INSERT INTO orders (summa, user_id, id) "
                         "VALUES (%s, %s, %s)" % (total, user_id, last_id + 1))
        for product in products:
            for _ in range(product[3]):
                self.cur.execute("INSERT INTO purchases (product_id, order_id) "
                                 "VALUES (%s, %s)" % (product[0], last_id + 1))

    def get_all_products(self, user_id):
        try:
            self.cur.execute("SELECT * FROM products")
            products = self.cur.fetchall()
            if user_id is None:
                return [tuple((*args, False)) for *args, in products]
            res = []
            self.cur.execute("SELECT product_id FROM favorites WHERE user_id = %s" % user_id)
            fav_ids = [product_id for product_id, in self.cur.fetchall()]
            for *args, in products:
                if args[-1] in fav_ids:
                    res.append(tuple((*args, True)))
                else:
                    res.append(tuple((*args, False)))
            if not res:
                return False
            return res
        except Exception as e:
            print(e)
            return False

    def get_all_favourites(self, user_id):
        try:
            self.cur.execute("SELECT id, title, description FROM products JOIN favorites f "
                             "ON products.id = f.product_id "
                             "WHERE user_id = %s" % user_id)
            res = self.cur.fetchall()
            if not res:
                return False
            return res
        except Exception as e:
            print(e)
            return False

    def is_product_favourite(self, product_id):
        self.cur.execute("SELECT * FROM favorites WHERE product_id = %s" % product_id)
        res = self.cur.fetchone()
        return bool(res)

    def add_to_favourite(self, user_id, product_id):
        try:
            self.cur.execute("INSERT INTO favorites (user_id, product_id) "
                             "VALUES (%s, %s)" % (user_id, product_id))
        except Exception as e:
            print(e)

    def delete_from_favourite(self, user_id, product_id):
        try:
            self.cur.execute("DELETE FROM favorites "
                             "WHERE user_id = %s and product_id = %s" % (user_id, product_id))
        except Exception as e:
            print(e)

    def get_cart(self, user_id):
        try:
            self.cur.execute("SELECT id, title, description, amount, cost, image_url FROM products JOIN "
                             "(SELECT user_id, product_id, count(*) amount FROM cart GROUP BY user_id, product_id) c "
                             "ON products.id = c.product_id "
                             "WHERE user_id = %s" % user_id)
            res = self.cur.fetchall()
            if not res:
                return False
            return res
        except Exception as e:
            print(e)
            return False

    def clear_cart(self, user_id):
        self.cur.execute("DELETE FROM cart WHERE user_id = %s" % user_id)

    def get_cart_with_total(self, user_id):
        products = self.get_cart(user_id)
        total = 0
        if products:
            for _, _, _, amount, cost, _ in products:
                total += amount * cost
        return products, total

    def add_to_cart(self, user_id, product_id):
        try:
            self.cur.execute("INSERT INTO cart (user_id, product_id) "
                             "VALUES (%s, %s)" % (user_id, product_id))
        except Exception as e:
            print(e)

    def delete_from_cart(self, user_id, product_id):
        try:
            self.cur.execute("DELETE FROM cart "
                             "WHERE user_id = %s and product_id = %s "
                             "and ctid = (select min(ctid) from cart "
                             "where user_id = %s and product_id = %s);" % (user_id, product_id, user_id, product_id))
        except Exception as e:
            print(e)

    def gen_prods(self):
        """Потом удалить"""
        for i in range(10):
            self.cur.execute("insert into products (title, description, gender, category, cost, image_url, id) "
                             "values ('title%d', 'desc%d', 'gender%d', 'cat%d', '%d', 'img%d', '%d')"
                             % (i, i, i, i, i, i, i))

    def gen_orders(self):
        """Потом удалить"""
        for i in range(10):
            self.cur.execute("insert into orders (summa, user_id, id) "
                             "values ('%d', 1, '%d')"
                             % (i * 100, i))

    def gen_purchs(self):
        """Потом удалить"""
        for i in range(10):
            self.cur.execute("insert into purchases (product_id, order_id) "
                             "values ('%d', '%d')"
                             % (random.randint(0, 9), i))
            self.cur.execute("insert into purchases (product_id, order_id) "
                             "values ('%d', '%d')"
                             % (random.randint(0, 9), i))
            self.cur.execute("insert into purchases (product_id, order_id) "
                             "values ('%d', '%d')"
                             % (random.randint(0, 9), i))

    def update_names(self, user_id, first_name, last_name):
        try:
            print('updating')
            self.cur.execute(
                "UPDATE users SET first_name='%s', last_name='%s' WHERE id=%s" % (first_name, last_name, user_id))
        except Exception as e:
            print(e)


class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.get_user_by_id(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # @property
    def get_id(self):
        return str(self.__user[0])

    @property
    def is_admin(self):
        return self.__user[6]
