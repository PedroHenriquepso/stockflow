from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

@router.post("/", response_model=schemas.VeiculoOut)
def criar(
    dados: schemas.VeiculoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.criar_veiculo(db, dados)

@router.get("/", response_model=list[schemas.VeiculoOut])
def listar(
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.listar_veiculos(db)

@router.get("/cliente/{cliente_id}", response_model=list[schemas.VeiculoOut])
def listar_por_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.buscar_veiculos_do_cliente(db, cliente_id)

@router.get("/buscar/{placa}", response_model=list[schemas.VeiculoOut])
def buscar_por_placa(
    placa: str,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.buscar_veiculos_por_placa(db, placa)