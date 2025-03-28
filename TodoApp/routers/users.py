from typing import Annotated
from fastapi import Depends, HTTPException, Path, APIRouter, Body
from sqlalchemy.orm import Session
from starlette import status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user, raise_401_could_not_validate_user, bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise_401_could_not_validate_user()
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT, description='Password successfully updated')
async def change_password(user: user_dependency, db: db_dependency,
                          old_password: str = Body(min_length=1, max_length=30),
                          new_password: str = Body(min_length=5, max_length=30)):
    if user is None:
        raise_401_could_not_validate_user()
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if bcrypt_context.verify(old_password, user_model.hashed_password):
        user_model.hashed_password = bcrypt_context.hash(new_password)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Wrong initial password')


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT, description="Phone number update")
async def update_phone_number(user: user_dependency, db: db_dependency,
                              phone_number: str = Body(min_length=5, max_length=15)):
    if user is None:
        raise_401_could_not_validate_user()
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.commit()
