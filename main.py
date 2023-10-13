from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Platillo(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float

class PlatilloDB(Base):
    __tablename__ = "platillos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
    precio = Column(Float)

Base.metadata.create_all(bind=engine)

@app.post("/platillos/", response_model=Platillo)
async def crear_platillo(platillo: Platillo, db: Session = Depends(get_db)):
    db_platillo = PlatilloDB(**platillo.dict())
    db.add(db_platillo)
    db.commit()
    db.refresh(db_platillo)
    db.close()
    return db_platillo

@app.get("/platillos/", response_model=List[Platillo])
async def leer_platillos(db: Session = Depends(get_db)):
    return db.query(PlatilloDB).all()

@app.get("/platillos/{platillo_id}", response_model=Platillo)
async def leer_platillo(platillo_id: int, db: Session = Depends(get_db)):
    db_platillo = db.query(PlatilloDB).filter(PlatilloDB.id == platillo_id).first()
    if not db_platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    return db_platillo

@app.put("/platillos/{platillo_id}", response_model=Platillo)
async def actualizar_platillo(platillo_id: int, platillo: Platillo, db: Session = Depends(get_db)):
    db_platillo = db.query(PlatilloDB).filter(PlatilloDB.id == platillo_id).first()
    if not db_platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    
    for key, value in platillo.dict().items():
        setattr(db_platillo, key, value)
    
    db.commit()
    db.refresh(db_platillo)
    return db_platillo

@app.delete("/platillos/{platillo_id}", response_model=Platillo)
async def borrar_platillo(platillo_id: int, db: Session = Depends(get_db)):
    db_platillo = db.query(PlatilloDB).filter(PlatilloDB.id == platillo_id).first()
    if not db_platillo:
        raise HTTPException(status_code=404, detail="Platillo no encontrado")
    
    db.delete(db_platillo)
    db.commit()
    return db_platillo
