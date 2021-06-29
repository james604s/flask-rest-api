import psycopg2
import psycopg2.extras
host = "localhost"
dbname = "flask_api"
dbuser= "sq"
dbpwd = "1234"
sslmode = "require"

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def db_init(self):
        try:
            db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        except:
            print("error message")
        #cursor_factory=
        else:
            #DictCursor不返回Dict, RealDict才返回 
            cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return db, cursor

    @classmethod
    def find_by_username(cls, username):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        sql = f"SELECT * FROM users WHERE username='{username}';"
        cursor.execute(sql)
        db.commit()
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        db.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        sql = f"SELECT * FROM users WHERE id='{_id}';"
        cursor.execute(sql)
        db.commit()
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        db.close()
        return user