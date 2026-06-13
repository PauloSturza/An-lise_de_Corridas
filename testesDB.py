import sqlite3

conn = sqlite3.connect("corridas.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM corridas")
tabela = cursor.fetchall()
print(tabela)