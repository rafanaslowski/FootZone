from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.db import conectar_banco

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# SCHEMAS
# --------------------
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class LoginData(BaseModel):
    email: str
    senha: str

# --------------------
# ROTAS
# --------------------
@app.get("/usuarios")
def buscar_usuarios():
    try:
        conn = conectar_banco()
        if conn is None:
            raise HTTPException(status_code=500, detail="Erro ao conectar no banco")

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nome, email FROM usuario")
        usuarios = cursor.fetchall()

        cursor.close()
        conn.close()
        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/usuarios", status_code=201)
def cadastrar_usuario(dados: UsuarioCreate):
    try:
        conn = conectar_banco()
        if conn is None:
            raise HTTPException(status_code=500, detail="Erro ao conectar no banco")

        cursor = conn.cursor()
        sql = "INSERT INTO usuario (nome, email, senha_hash) VALUES (%s, %s, %s)"
        cursor.execute(sql, (dados.nome, dados.email, dados.senha))
        conn.commit()

        cursor.close()
        conn.close()
        return {"mensagem": "Usuário salvo com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def login(dados: LoginData):
    try:
        conn = conectar_banco()
        if conn is None:
            raise HTTPException(status_code=500, detail="Erro ao conectar no banco")

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s"
        cursor.execute(sql, (dados.email, dados.senha))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return {"status": "sucesso", "nome": usuario["nome"]}

        raise HTTPException(status_code=401, detail="Login inválido")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
