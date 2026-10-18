from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.routers import produtos, clientes, vendas, auth, veiculos, orcamentos

Base.metadata.create_all(bind=engine) 

from app.database import SessionLocal
from app import models

# Cria o Consumidor Padrão se não existir
db = SessionLocal()
if not db.query(models.Cliente).filter(models.Cliente.id == 1).first():
    consumidor = models.Cliente(
        id=1, 
        nome="CONSUMIDOR", 
        cpf_cnpj="00000000000",
        email="consumidor@padrao.com"
    )
    db.add(consumidor)
    db.commit()
db.close()

app = FastAPI(title="StockFlow API", version="0.2.0")

# Rotas da API (JSON)
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(clientes.router)
app.include_router(vendas.router)
app.include_router(veiculos.router)
app.include_router(orcamentos.router)

# Arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Rota raiz: serve a tela de login
@app.get("/")
def raiz():
    return FileResponse("frontend/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/dashboard.html")

@app.get("/produtos")
def tela_produtos():
    return FileResponse("frontend/produtos.html")

@app.get("/orcamentos")
def tela_lista_orcamentos():
    return FileResponse("frontend/orcamentos.html")

@app.get("/orcamentos/novo")
def tela_novo_orcamento():
    return FileResponse("frontend/orcamentos_novo.html")