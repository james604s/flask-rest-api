import psycopg2
import psycopg2.extras
from flask_restful import Resource, reqparse
host = "localhost"
dbname = "flask_api"
dbuser= "sq"
dbpwd = "1234"
sslmode = "require"
class User:
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

class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank.")

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        password = data['password']

        if User.find_by_username(username):
            return {"message": "A user with that username already exists"}, 400

        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()

        sql = f"INSERT INTO users(id, username, password) VALUES (NULL, '{username}','{password}')"
        cursor.execute(sql)
        
        db.commit()
        db.close()
        return {"message":"User created successfully."}, 201