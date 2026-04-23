import os
import hashlib
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import conectar_banco 

app = FastAPI()

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

# Configuração para buscar as pastas fora de /backend
app.mount("/Static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "Static")), name="static")
app.mount("/Imagens", StaticFiles(directory=os.path.join(BASE_DIR, "..", "Imagens")), name="imagens")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "Template"))

# --- HELPER: VERIFICAR LOGIN ---
def get_usuario_logado(request: Request):
    return request.cookies.get("usuario_nome")

# --- ROTAS DE NAVEGAÇÃO ---

@app.get("/", response_class=HTMLResponse)
@app.get("/catalogo", response_class=HTMLResponse)
async def page_catalogo(request: Request):
    usuario = get_usuario_logado(request)
    logado = usuario is not None
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.*, i.url 
            FROM produto p 
            LEFT JOIN produto_imagem i ON p.id_produto = i.id_produto 
            GROUP BY p.id_produto
        """
        cursor.execute(query)
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        produtos = []

    return templates.TemplateResponse("catalogo.html", {
        "request": request, 
        "produtos": produtos, 
        "logado": logado, 
        "usuario": usuario
    })

# Rota para abrir a tela de Login de Usuário
@app.get("/login", response_class=HTMLResponse)
async def page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota para abrir a tela de Admin
@app.get("/admin", response_class=HTMLResponse)
async def page_admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# NOVA ROTA: Rota para abrir a tela de Cadastro (usuario.html)
@app.get("/cadastro", response_class=HTMLResponse)
async def page_cadastro(request: Request):
    return templates.TemplateResponse("usuario.html", {"request": request})

# --- PROCESSAMENTO DE LOGIN ---

@app.post("/login/usuario")
async def login_usuario(email: str = Form(...), senha: str = Form(...)):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    
    # Hash da senha para conferência
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    
    query = "SELECT nome FROM usuario WHERE email = %s AND senha_hash = %s"
    cursor.execute(query, (email, senha_hash))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        response = RedirectResponse(url="/catalogo", status_code=303)
        response.set_cookie(key="usuario_nome", value=user['nome'], httponly=True)
        return response
    
    raise HTTPException(status_code=401, detail="Email ou Senha incorretos")

@app.post("/login/admin")
async def login_admin(email: str = Form(...), chave: str = Form(...)):
    conn = conectar_banco()
    cursor = conn.cursor(dictionary=True)
    chave_hash = hashlib.sha256(chave.encode()).hexdigest()
    
    query = """
        SELECT u.nome FROM usuario u 
        JOIN admin a ON u.id_usuario = a.id_usuario 
        WHERE u.email = %s AND a.chave_acesso = %s
    """
    cursor.execute(query, (email, chave_hash))
    admin = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if admin:
        response = RedirectResponse(url="/catalogo", status_code=303)
        response.set_cookie(key="admin_logado", value="true", httponly=True)
        response.set_cookie(key="usuario_nome", value=admin['nome'], httponly=True)
        return response
    
    raise HTTPException(status_code=401, detail="Credenciais Inválidas")

# --- NOVA ROTA DE CADASTRO ---
@app.post("/cadastrar/usuario")
async def cadastrar_usuario(
    nome: str = Form(...),
    cpf: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...)
):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Hash da senha
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    try:
        # 1. Inserir na tabela pai (usuario)
        query_user = """
            INSERT INTO usuario (nome, email, senha_hash)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_user, (nome, email, senha_hash))
        
        # Pega o ID que acabou de ser gerado
        id_novo_usuario = cursor.lastrowid

        # 2. Inserir na tabela filha (cliente) os dados específicos
        # Remove pontos e traços do CPF se necessário antes de salvar
        cpf_limpo = ''.join(filter(str.isdigit, cpf)) 
        
        query_cliente = """
            INSERT INTO cliente (id_usuario, cpf, telefone)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query_cliente, (id_novo_usuario, cpf_limpo, telefone))

        # Confirma as duas transações
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar: {e}") # Log para você debugar no terminal
        raise HTTPException(status_code=400, detail="Erro ao cadastrar usuário. Verifique se o e-mail ou CPF já existem.")
    
    finally:
        cursor.close()
        conn.close()

    return RedirectResponse(url="/login", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("admin_logado")
    response.delete_cookie("usuario_nome")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)