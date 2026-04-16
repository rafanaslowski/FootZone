from flask import Flask, request, jsonify
from flask_cors import CORS
from db import conectar_banco

app = Flask(__name__)
CORS(app)

@app.route('/usuarios', methods=['GET'])
def buscar_usuarios():
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        # SELECT que você vai mostrar para os professores
        cursor.execute("SELECT id_usuario, nome, email FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.json
        conn = conectar_banco()
        cursor = conn.cursor()
        # Ajustado para 'senha_hash' conforme seu erro anterior
        sql = "INSERT INTO usuario (nome, email, senha_hash) VALUES (%s, %s, %s)"
        valores = (dados['nome'], dados['email'], dados['senha'])
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensagem": "Usuário salvo com sucesso!"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        dados = request.json
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        # SELECT com filtro para a tela de login
        sql = "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s"
        cursor.execute(sql, (dados['email'], dados['senha']))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            return jsonify({"status": "sucesso", "nome": usuario['nome']}), 200
        return jsonify({"status": "erro", "mensagem": "Login inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)