import psycopg2
import psycopg2.extras
host = "localhost"
dbname = "flask_api"
dbuser= "sq"
dbpwd = "1234"
sslmode = "require"

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price= price
    
    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()

        query = f"SELECT * FROM items WHERE name='{name}'"
        cursor.execute(query)
        row = cursor.fetchone()
        db.close()
        if row:
            return cls(*row)
            # return cls(row[0], row[1])
        # return {"message": "Item not found."}, 404

    def insert(self):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        
        q = f"INSERT INTO items VALUES ('{self.name}',{self.price})"
        cursor.execute(q)

        db.commit()
        db.close()

    def update(self):
        db = psycopg2.connect(database=dbname,user=dbuser, password=dbpwd, host=host, port="5432")
        cursor = db.cursor()
        
        q = f"UPDATE items SET price={self.price} WHERE name='{self.name}'"
        cursor.execute(q)

        db.commit()
        db.close()