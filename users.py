
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, Session
import model, schema, utils
from database import get_db
router = APIRouter(
    prefix="/users", # Prefix for all routes in this router
    tags=['Users'] # Tags for all routes in this router. It helps in grouping the routes in the documentation
)



@router.post("/", response_model=schema.UserCreate, status_code= status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db: Session= Depends(get_db)):
    try:
        # Hash the password before storing it into the DB
        # print(user.password)
        user.password = utils.hash(user.password)
        # print(user.password)
        db_user = model.Users(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return db_user
