from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.post("/", response_model=schemas.VendaOut)
def criar(
    dados: schemas.VendaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.criar_venda(db, dados)

@router.get("/", response_model=list[schemas.VendaOut])
def listar(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.listar_vendas(db)

@router.get("/{venda_id}", response_model=schemas.VendaOut)
def buscar(
    venda_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.buscar_venda(db, venda_id)