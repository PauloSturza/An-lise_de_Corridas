import sqlite3

def iniciar_banco():
    conn = sqlite3.connect('corridas.db')
    conn.execute("PRAGMA foreign_keys = ON")

    cursor = conn.cursor()

    cursor.execute('CREATE TABLE  IF NOT EXISTS tenis (tenis_id INTEGER PRIMARY KEY AUTOINCREMENT, tenis TEXT )')


    #Colunas: id, teis_id, distancia, tempo, data
    cursor.execute('CREATE TABLE IF NOT EXISTS corridas (id INTEGER PRIMARY KEY AUTOINCREMENT, tenis_id INTEGER REFERENCES tenis(tenis_id), distancia REAL, tempo REAL, data TEXT)')
    
    cursor.execute("SELECT * FROM corridas")
    resultado = cursor.fetchall()
    if len(resultado) == 0:
        cursor.execute("INSERT INTO tenis VALUES (NULL,'nimbus')")
        cursor.execute("INSERT INTO tenis VALUES (NULL,'fila')")
        cursor.execute("INSERT INTO corridas VALUES (NULL, 1, 10, 55, '2026-01-01')")
        cursor.execute("INSERT INTO corridas VALUES (NULL, 1, 9.5, 52, '2026-01-02')")
        cursor.execute("INSERT INTO corridas VALUES (NULL, 1, 9.8, 53, '2026-01-03')")

    conn.commit()
    conn.close()