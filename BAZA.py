import sqlite3

base = sqlite3.connect("filename.db")
cursor = base.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS yeat(ID INTEGER, NAME TEXT, USERNAME TEXT, DATE INTEGER)")

cursor.execute("""INSERT INTO yeat(ID, NAME, USERNAME, DATE) VALUES(1, "Платина", "sosamuzik300", 1706/2024)""")
base.commit()
cursor.execute("""SELECT * FROM yeat""")
fullbase = cursor.fetchmany(3)
# fullbase = cursor.fetchone()
# fullbase = cursor.fetchall()
print(fullbase)

cursor.execute("""UPDATE yeat SET NAME="BOTTEGABOI" WHERE ID=4""")
base.commit()

cursor.execute("""DELETE FROM yeat WHERE ID=2""")
base.commit()

with sqlite3.connect("filename.db") as f:
    cursor = f.cursor()
