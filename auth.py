
from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker, Session
import model, schema, utils, OAuth2
from database import get_db

router = APIRouter(
    prefix="", # Prefix for all routes in this router
    tags=['Authentication']
)

@router.post("/login/", response_model=schema.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(model.Users).filter(model.Users.user_id == form_data.username).first()
    print(f'Form data : {form_data.username}  {form_data.password}')
    print(f'DB user data : {db_user}')
    if not db_user or not utils.verify(form_data.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = OAuth2.create_access_token(data={"sub": db_user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
