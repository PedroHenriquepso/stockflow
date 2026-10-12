from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.post("/", response_model=schemas.VendaOut)
def criar(dados: schemas.VendaCreate, db: Session = Depends(get_db)):
    return crud.criar_venda(db, dados)

@router.get("/", response_model=list[schemas.VendaOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_vendas(db)

@router.get("/{venda_id}", response_model=schemas.VendaOut)
def buscar(venda_id: int, db: Session = Depends(get_db)):
    return crud.buscar_venda(db, venda_id)