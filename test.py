import psycopg2
import psycopg2.extras
host = "localhost"
dbname = "flask_api"
usern = "sq"
password = "1234"
sslmode = "require"

db = psycopg2.connect(database=dbname,user=usern, password=password, host=host, port="5432")
cursor = db.cursor()
sql = f"SELECT * FROM user_test WHERE id=1"
cursor.execute(sql)
db.commit()
row = cursor.fetchone()
print(row)
db.close()
