from sqlmodel import SQLModel, Field

# Crea una tabla
class product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key = True)
    name: str
    lastname: str
    precio: float
    cantidad: int
    pes: float

# Plantilla para creacion de un usuario
class Requisitos(SQLModel):
    name: str
    lastname: str
    precio: float
    cantidad: int
    pes: float

# Son los datos que devolveria
class resposta(SQLModel):
    id: int
    name: str
    lastname: str
    cantidad: int

# Son los datos que devolveria con 3 datos
class respostaCorta(SQLModel):
    id: int
    name: str
    lastname: str