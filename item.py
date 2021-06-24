import psycopg2
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

host = "localhost"
dbname = "flask_api"
dbuser= "sq"
dbpwd = "1234"
sslmode = "require"

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found."}, 404
        # item = list(filter(lambda x: x['name'] ==name, items))
        # item = next(filter(lambda x: x['name'] ==name, items), None)
        # return {"item":None}, 200 if item else 404
    @classmethod
    def find_by_name(cls, name):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()

        query = f"SELECT * FROM items WHERE name='{name}'"
        cursor.execute(query)
        row = cursor.fetchone()
        db.close()
        if row:
            return {"item":{"name": row[1], "price": row[2]}}
        # return {"message": "Item not found."}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {"message":f"An item with name '{name}' already exists."}, 400
        # if next(filter(lambda x: x['name'] ==name, items), None) is not None:
        #     return {"message":f"An item with name '{name}' already exists."}, 400
        data = Item.parser.parse_args()
        
        item = {"name":name, "price":data['price']}
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        
        q = f"INSERT INTO items VALUES ('{item['name']}',{item['price']})"
        cursor.execute(q)

        db.commit()
        db.close()
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] !=name, items))
        return {"message": "Item deleted"}
    
    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {"name": name, "price":data["price"]}
            items.append(item)
        item.update(data)
        return item
class ItemList(Resource):
    def get(self):
        return {"items": items}