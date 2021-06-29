import psycopg2
import psycopg2.extras
from flask_restful import Resource, reqparse
from models.user import UserModel
host = "localhost"
dbname = "flask_api"
dbuser= "sq"
dbpwd = "1234"
sslmode = "require"
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

        if UserModel.find_by_username(username):
            return {"message": "A user with that username already exists"}, 400

        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()

        sql = f"INSERT INTO users(id, username, password) VALUES (NULL, '{username}','{password}')"
        cursor.execute(sql)
        
        db.commit()
        db.close()
        return {"message":"User created successfully."}, 201