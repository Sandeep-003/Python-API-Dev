from jose import jwt, JWTError
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from database import get_db

SECRET_KEY = "b7f8e2c9d4a1e6f3b0c5d8a2f1e4c7b9a6d3f0b2e5c8a1d4f7b2c9e6a3d0f5b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_token(token: str, credentials_exception):
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    return payload  

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = verify_token(token, credentials_exception)
        print(f'Payload: {payload}')
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = db.query(model.Users).filter(model.Users.user_id == user_id).first()
        if user is None:
            raise credentials_exception
        # print(f'Current authorized user ID: {user.user_id}')
        return user
    except JWTError:
        raise credentials_exception   

# Example usage in a FastAPI route 
# @app.get("/protected-route/")
# def protected_route(current_user: model.Users = Depends(get_current_user)):
#     return {"msg": f"Hello, {current_user.name}"}
#
# The tokenUrl in OAuth2PasswordBearer should point to the login endpoint where the token is generated.
# The get_current_user function can be used as a dependency in any route that requires authentication.  
# This function will decode the JWT token, verify its validity, and fetch the corresponding user from the database. 
# If the token is invalid or the user does not exist, it raises an HTTP 401 Unauthorized exception.

# You can use the create_access_token function to generate a JWT token after a user successfully logs in.
# The token will include the user's ID and an expiration time.
# Example of generating a token after user login:
# user = db.query(model.Users).filter(model.Users.user_id == user_id).first()   
# if user:
#     access_token = create_access_token(data={"sub": user.user_id})
#     return {"access_token": access_token, "token_type": "bearer"}
# The token can then be used in the Authorization header of subsequent requests to access protected routes.
# Example of using the token in a request header:
# headers = {"Authorization": f"Bearer {access_token}"}
# response = client.get("/protected-route/", headers=headers)

# Always ensure to follow best security practices when handling authentication and sensitive data.
# For more advanced use cases, consider implementing scopes and roles to manage user permissions.       
# You can also customize the payload of the JWT token to include additional user information as needed.
