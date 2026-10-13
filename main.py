from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import Base, engine
from app.routers import produtos, clientes, vendas, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockFlow API", version="0.2.0")

# Rotas da API (JSON)
app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(clientes.router)
app.include_router(vendas.router)

# Arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Rota raiz: serve a tela de login
@app.get("/")
def raiz():
    return FileResponse("frontend/index.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("frontend/dashboard.html")