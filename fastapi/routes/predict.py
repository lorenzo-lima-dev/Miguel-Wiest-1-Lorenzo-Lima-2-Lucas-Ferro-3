from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.database import get_session
from fastapi.models.schemas import Prediction, PredictionCreate, User
from fastapi.security.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

@router.post("/")
def create_pred(pred_in: PredictionCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    new_pred = Prediction(owner_id=current_user.id, input_text=pred_in.input_text, result="Processado: " + pred_in.input_text[:5])
    session.add(new_pred)
    session.commit()
    session.refresh(new_pred)
    return new_pred

@router.get("/{pred_id}")
def get_pred(pred_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    pred = session.get(Prediction, pred_id)
    if not pred or pred.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Recurso não encontrado ou acesso negado (BOLA)")
    return pred
