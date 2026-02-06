from fastapi import FastAPI,HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from schemas import Valentine_name,UserCreate,UserLogin
from model import Valentine,User
from database import SessionLocal,engine,Base
import secrets

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security)
):
    db = SessionLocal()
    user = db.query(User).filter(User.email == credentials.username).first()

    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not secrets.compare_digest(user.password, credentials.password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db.close()
    return user

@app.post('/valentine')
def create_valentine(data: Valentine_name,user: User = Depends(get_current_user)):
    db = SessionLocal()
    entry = Valentine(name=data.name,user=user.id)
    db.add(entry)
    db.commit()
    db.close()
    print(data)
    return {
        "message":"Happy Valentine's Day",
        "name":data.name,
        "by":user.email
    }
@app.post('/signup')
def signup(data: UserCreate):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, password=data.password,Fullname=data.name)
    db.add(user)
    db.commit()
    db.close()
    return {
        "message":"User created successfully",
    }
@app.post('/login')
def login(data: UserLogin):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email, User.password == data.password).first()
    db.close()
    if user:
        return {
            "success":True,
            "message":"Login successful",
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
@app.get('/users_valentines')
def get_users_valentines(user: User = Depends(get_current_user)):
    db = SessionLocal()
    valentines = db.query(Valentine).filter(Valentine.user==user.id).all()
    db.close()
    result = [{"id":v.id,"name":v.name} for v in valentines]
    return result

