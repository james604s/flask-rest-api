import psycopg2
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found."}, 404
        # item = list(filter(lambda x: x['name'] ==name, items))
        # item = next(filter(lambda x: x['name'] ==name, items), None)
        # return {"item":None}, 200 if item else 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message":f"An item with name '{name}' already exists."}, 400
        # if next(filter(lambda x: x['name'] ==name, items), None) is not None:
        #     return {"message":f"An item with name '{name}' already exists."}, 400
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {"message":"An error occured inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        
        q = f"DELETE FROM items WHERE name='{name}')"
        cursor.execute(q)

        db.commit()
        db.close()
        # global items
        # items = list(filter(lambda x: x['name'] !=name, items))
        return {"message": "Item deleted"}
    
    def put(self, name):
        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data["price"])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message":"An error occurred inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message":"An error occurred updating the item"}, 500
        return updated_item.json()
class ItemList(Resource):
    def get(self):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        
        q = "SELECT * FROM items"
        result = cursor.execute(q)
        
        items = [{'name':row[1], 'price':row[2]} for row in result]
        # db.commit()
        db.close()
        return {"items": items}