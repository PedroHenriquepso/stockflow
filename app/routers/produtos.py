from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=schemas.ProdutoOut)
def criar(dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, dados)

@router.get("/", response_model=list[schemas.ProdutoOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def buscar(produto_id: int, db: Session = Depends(get_db)):
    return crud.buscar_produto(db, produto_id)

@router.put("/{produto_id}", response_model=schemas.ProdutoOut)
def atualizar(produto_id: int, dados: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.atualizar_produto(db, produto_id, dados)

@router.delete("/{produto_id}")
def deletar(produto_id: int, db: Session = Depends(get_db)):
    return crud.deletar_produto(db, produto_id)