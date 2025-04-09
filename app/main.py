from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .models.user import UserCreate, User, UserUpdate
from .services.user_service import UserService
from .repositories.user_repository import SessionLocal

app = FastAPI(title="Demo API")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Demo"}

@app.get("/user", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    try:
        return UserService.get_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@app.put("/user/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = UserService.update_user(db, user_id, user.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return updated_user

@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not UserService.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")