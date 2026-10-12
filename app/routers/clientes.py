from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteOut)
def criar(dados: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.criar_cliente(db, dados)

@router.get("/", response_model=list[schemas.ClienteOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_clientes(db)

@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def buscar(cliente_id: int, db: Session = Depends(get_db)):
    return crud.buscar_cliente(db, cliente_id)