from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.schemas.Client import Client
from app.utils.security import Security

router = APIRouter()
security = Security()
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/create_client")
async def create_user(db: db_dependency, client: Client):
    try:
        hashed_password = security.get_password_hash(client.mdp)
        client.mdp = hashed_password
        Client.create_user(client, db)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@router.post("/token")
async def login_for_access_token(db: db_dependency, username: str, password: str):
    user = Client.get_client(db, username)
    if user and security.verify_password(password, user.mdp):
        user.mdp = ""
        token_data = user.dict()
        access_token = security.create_access_token(token_data)
        return {"access_token": access_token, "token_type": "bearer", "user_object": user.dict()}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/get_user_from_token")
async def get_user_from_token(token: str):
    try:
        current_user = security.decode_token(token)
        return {"message": "This is a protected route", "user": current_user}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
        )
