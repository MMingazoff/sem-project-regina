import psycopg2


class DataBase:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="#ur name",
            user="#ur user",
            password="#ur password",
            host="#ur localhost",
            port=5432
        )
        self.con.autocommit = True
        self.cur = self.con.cursor()

    def get_user_by_id(self, user_id):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.cur.fetchone()
            if not res:
                print("User not find")
                return False
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


class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.get_user_by_id(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])
