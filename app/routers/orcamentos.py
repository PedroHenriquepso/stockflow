from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/orcamentos", tags=["Orçamentos"])

@router.post("/", response_model=schemas.OrcamentoOut)
def criar(
    dados: schemas.OrcamentoCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.criar_orcamento(db, dados, usuario.id)

@router.get("/", response_model=list[schemas.OrcamentoOut])
def listar(
    status: str = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    return crud.listar_orcamentos(db, status=status)