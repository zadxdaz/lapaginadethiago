import sqlite3
conector=sqlite3.connect("test.db")
cursor=conector.cursor()

def eliminartodo(cursor,con):
    cursor.execute("DELETE FROM Item")
    con.commit()

#eliminartodo(cursor,conector)///
lista=cursor.execute("SELECT * FROM marcas")
print(type(lista))
for row in lista:
   print(row)
"""
marcas=("chevrolet","fiat","wolkswagen","BMW","honda","toyota")
for x in marcas:
    query="INSERT INTO marcas(marca) VALUES ('" + x + "')"
    l=cursor.execute(query)
    conector.commit()
"""


