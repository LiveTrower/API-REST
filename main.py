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

class Helado(BaseModel):
    sabor: str
    precio: float

class HeladoDB(Base):
    __tablename__ = "helados"

    id = Column(Integer, primary_key=True, index=True)
    sabor = Column(String, index=True)
    precio = Column(Float)

Base.metadata.create_all(bind=engine)

@app.post("/sabores/", response_model=Helado)
async def crear_sabor(Helado: Helado, db: Session = Depends(get_db)):
    db_Helado = HeladoDB(**Helado.dict())
    db.add(db_Helado)
    db.commit()
    db.refresh(db_Helado)
    db.close()
    return db_Helado

@app.get("/sabores/", response_model=List[Helado])
async def leer_sabores(db: Session = Depends(get_db)):
    return db.query(HeladoDB).all()

@app.get("/sabores/{sabor_id}", response_model=Helado)
async def leer_sabor(Helado_id: int, db: Session = Depends(get_db)):
    db_Helado = db.query(HeladoDB).filter(HeladoDB.id == Helado_id).first()
    if not db_Helado:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return db_Helado

@app.put("/sabores/{sabor_id}", response_model=Helado)
async def actualizar_sabor(Helado_id: int, Helado: Helado, db: Session = Depends(get_db)):
    db_Helado = db.query(HeladoDB).filter(HeladoDB.id == Helado_id).first()
    if not db_Helado:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    
    for key, value in Helado.dict().items():
        setattr(db_Helado, key, value)
    
    db.commit()
    db.refresh(db_Helado)
    return db_Helado

@app.delete("/sabores/{sabor_id}", response_model=Helado)
async def borrar_sabor(Helado_id: int, db: Session = Depends(get_db)):
    db_Helado = db.query(HeladoDB).filter(HeladoDB.id == Helado_id).first()
    if not db_Helado:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    
    db.delete(db_Helado)
    db.commit()
    return db_Helado
