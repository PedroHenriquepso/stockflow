from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.security import criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar", response_model=schemas.UsuarioOut)
def registrar(dados: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.criar_usuario(db, dados)

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    usuario = crud.autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = criar_token_acesso({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}