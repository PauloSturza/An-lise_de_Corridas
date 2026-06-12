import sqlite3

def distancia_total_corrida():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(distancia) FROM corridas")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado[0] is not None else 0.0


def lista_tenis():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tenis,tenis_id FROM tenis")
    resultado = cursor.fetchall()
    conn.close()
    return resultado 

def lancar_corrida_db(tenis_id, distancia, tempo, data):
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO corridas (tenis_id, distancia, tempo, data) VALUES ( ?, ?, ?, ?)",(tenis_id, distancia, tempo, data))
    conn.commit()
    conn.close()

def historico_corridas():
    conn = sqlite3.connect("corridas.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.data, t.tenis, c.distancia, c.tempo
    FROM corridas AS c
    JOIN tenis AS t ON C.tenis_id = t.tenis_id
    ORDER BY c.data DESC
    """)
    resultado = cursor.fetchall()

    conn.close()
    return resultado