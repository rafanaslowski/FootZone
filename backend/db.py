import mysql.connector

def conectar_banco():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="PUC@1234",
            database="marketplace_tenis"
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar no banco: {err}")
        return None
