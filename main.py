from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import os

db_config = {
    'host': os.getenv("MYSQL_SERVICE_HOST"),
    'user': 'root',
    'passwd': os.getenv("db_root_password"),
    'db': os.getenv("db_name"),
    'port': 3306,
}

conn = mysql.connector.connect(**db_config)

app = FastAPI()

class Helado(BaseModel):
    sabor: str
    precio: float

@app.post("/sabores/", response_model=Helado)
async def crear_sabor(Helado: Helado):
    cursor = conn.cursor()
    query = "INSERT INTO helados(sabor, precio) VALUES(%s, %s)"
    cursor.execute(query, (Helado.sabor, Helado.precio))
    conn.commit()
    cursor.close()
    return Helado

@app.get("/sabores/", response_model=List[Helado])
async def leer_sabores():
    cursor = conn.cursor()
    query = "SELECT * FROM helados"
    cursor.execute(query)
    items = cursor.fetchall()
    cursor.close()
    return [{"id": item[0], "sabor": item[1], "precio": item[2]} for item in items]

@app.get("/sabores/{sabor_id}", response_model=Helado)
async def leer_sabor(Helado_id: int):
    cursor = conn.cursor()
    query = "SELECT id, sabor, precio FROM helados WHERE id=%s"
    cursor.execute(query, (Helado_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return {"id": item[0], "sabor": item[1], "precio": item[2]}

@app.put("/sabores/{sabor_id}", response_model=Helado)
async def actualizar_sabor(Helado_id: int, Helado: Helado):
    cursor = conn.cursor()
    query = "UPDATE helados SET sabor=%s, precio=%s WHERE id=%s"
    cursor.execute(query, (Helado.sabor, Helado.precio, Helado_id))
    conn.commit()
    cursor.close()
    return Helado

@app.delete("/sabores/{sabor_id}", response_model=Helado)
async def borrar_sabor(Helado_id: int):
    cursor = conn.cursor()
    query = "DELETE FROM helados WHERE id=%s"
    cursor.execute(query, (Helado_id,))
    conn.commit()
    cursor.close()
    return {"id": Helado_id}
