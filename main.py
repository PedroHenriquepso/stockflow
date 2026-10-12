from fastapi import FastAPI
from app.database import Base, engine
from app.routers import produtos, clientes, vendas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockFlow API", version="0.1.0")

app.include_router(produtos.router)
app.include_router(clientes.router)
app.include_router(vendas.router)

@app.get("/")
def raiz():
    return {"status": "ok", "sistema": "StockFlow", "versao": "0.1.0"}