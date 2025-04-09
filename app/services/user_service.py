import hashlib
from sqlalchemy.orm import Session
from ..models.user import UserCreate, User
from ..repositories.user_repository import UserModel

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha512(password.encode()).hexdigest()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = UserService.hash_password(user.password)
        db_user = UserModel(
            login=user.login,
            password=hashed_password,
            name=user.name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_users(db: Session):
        return db.query(UserModel).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: dict):
        db_user = UserService.get_user_by_id(db, user_id)
        if db_user:
            for key, value in user_data.items():
                if key == "password":
                    value = UserService.hash_password(value)
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        db_user = UserService.get_user_by_id(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False