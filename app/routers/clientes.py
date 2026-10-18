from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteOut)
def criar(dados: schemas.ClienteCreate, db: Session = Depends(get_db), usuario: models.Usuario = Depends(obter_usuario_atual)):
    return crud.criar_cliente(db, dados)

@router.get("/", response_model=list[schemas.ClienteOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_clientes(db)

@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def buscar(cliente_id: int, db: Session = Depends(get_db)):
    return crud.buscar_cliente(db, cliente_id)

@router.get("/buscar/{termo}", response_model=list[schemas.ClienteOut])
def buscar_por_termo(
    termo: str,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.buscar_clientes_por_termo(db, termo)