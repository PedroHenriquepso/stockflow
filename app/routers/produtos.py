from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=schemas.ProdutoOut)
def criar(
    dados: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.criar_produto(db, dados)

@router.get("/", response_model=list[schemas.ProdutoOut])
def listar(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.listar_produtos(db)

@router.get("/{produto_id}", response_model=schemas.ProdutoOut)
def buscar(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.buscar_produto(db, produto_id)

@router.put("/{produto_id}", response_model=schemas.ProdutoOut)
def atualizar(
    produto_id: int,
    dados: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.atualizar_produto(db, produto_id, dados)

@router.delete("/{produto_id}")
def deletar(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.deletar_produto(db, produto_id)