import os
import uvicorn
import hashlib  # Biblioteca nativa, não precisa instalar nada
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import conectar_banco 

app = FastAPI()

# Configuração de Caminhos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/Static", StaticFiles(directory=os.path.join(BASE_DIR, "Static")), name="static")
app.mount("/Imagens", StaticFiles(directory=os.path.join(BASE_DIR, "Imagens")), name="imagens")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "Template"))

# --- ROTAS DE NAVEGAÇÃO ---
@app.get("/", response_class=HTMLResponse)
@app.get("/usuario", response_class=HTMLResponse)
async def page_usuario(request: Request):
    return templates.TemplateResponse(request=request, name="usuario.html")

@app.get("/empresa", response_class=HTMLResponse)
async def page_empresa(request: Request):
    return templates.TemplateResponse(request=request, name="empresa.html")

@app.get("/admin", response_class=HTMLResponse)
async def page_admin(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html")

@app.get("/catalogo", response_class=HTMLResponse)
async def page_catalogo(request: Request):
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT p.*, i.url FROM produto p LEFT JOIN produto_imagem i ON p.id_produto = i.id_produto GROUP BY p.id_produto")
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()
        return templates.TemplateResponse(request=request, name="catalogo.html", context={"produtos": produtos})
    except:
        return templates.TemplateResponse(request=request, name="catalogo.html", context={"produtos": []})

# --- PROCESSAMENTO ---
@app.post("/cadastrar/usuario")
async def cadastrar_usuario(nome: str = Form(...), email: str = Form(...), senha: str = Form(...), cpf: str = Form(...), telefone: str = Form(...)):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # APLICANDO O HASH: Transforma a senha em SHA-256 antes de enviar ao banco
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    try:
        # Agora salvamos 'senha_hash' em vez da senha aberta
        cursor.execute("INSERT INTO usuario (nome, email, senha_hash) VALUES (%s, %s, %s)", (nome, email, senha_hash))
        id_user = cursor.lastrowid
        cursor.execute("INSERT INTO cliente (id_usuario, cpf, telefone) VALUES (%s, %s, %s)", (id_user, cpf.replace(".","").replace("-",""), telefone))
        conn.commit()
        return RedirectResponse(url="/catalogo", status_code=303)
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/login/admin")
async def login_admin(email: str = Form(...), chave: str = Form(...)):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT u.nome FROM usuario u JOIN admin a ON u.id_usuario = a.id_usuario WHERE u.email = %s AND a.chave_acesso = %s", (email, chave))
    if cursor.fetchone():
        return RedirectResponse(url="/catalogo", status_code=303)
    raise HTTPException(status_code=401, detail="Credenciais Inválidas")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)