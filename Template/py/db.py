import mysql.connector

# Esta função é o seu "túnel" lógico
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # usuário padrão do MySQL
            password="PUC@1234",      # sua senha (deixe vazio se não tiver)
            database="footzone" # Nome do banco que você criou no SQL [cite: 38, 44]
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro de conexão: {err}")
        return None