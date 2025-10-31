from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select, update
from dotenv import load_dotenv
from product import * # Importamos todo ya que necesitabamos todo, ahi la incongruencia
# Coger variables de un yml
from pydantic import BaseModel
# BaseModel sirve para asegurar que te pasen los datos en un formato de str, int especifico
import os # Necesiamos importar el OS para coger tambien la variable en el otro archivo
app = FastAPI()

load_dotenv()
    # Ejecutar docker docker-compose -f .\dockerFile.yaml up
DATABASE_URL = os.getenv("URL") # Importamos el echo que podamos coger esa variable
engine = create_engine(DATABASE_URL) # Cojemos el URL del otro fichero

# Esto crea la base de datos y los carga
SQLModel.metadata.create_all(engine)

# Cierra la base de datos cuando se acaba de hacer
def get_db():
    db = Session(engine) # Inicia una nueva sesion a traves de la URL cogida
    try: # Mientras funcione
        yield db # yield significa que lo coges en cualquier momento en el proyecto
    finally: # Cuando finalicemos o pete por un error se autocerrada
        db.close()

# Ex1
@app.post("/user", tags=["Create"], response_model=dict)
def addUser(user: Requisitos, db:Session = Depends(get_db)):
    # Cogera la clase usuario como plantilla y hara una sesion con la bbdd
    insertar = product.model_validate(user) # Le damos acceso a pasar por la plantilla de product para validar si es correcto
    # Convierte la entrada de Python a un lenguaje para SQL, como un traductor
    db.add(insertar) # Insertamos dentro de la tabla el user nuevo
    db.commit() # Guardamos cambios
    # Inserta los campos y el commit inserta los cambios
    return {"msg":"Afegit usuari correctament"} # Mensaje de muestra

# Ex2
@app.get("/user/{id}", tags=["Consult"], response_model=product)
def findUser(id: int, db: Session = Depends(get_db)):
    # Poner consulta en una variable
    buscar = select(product).where(product.id == id) # Cogeremos exactamente solo los o el usuario con ese ID
    # Ejecutar la consulta
    result = db.exec(buscar).first() # Cogeremos solo 1 resultado, usualmente el que esta mas arriba
    return result # Devolvemos el usuario que hemos buscado

# Ex3
# Busca tots els usuaris, eliminan les dades sensibles
@app.get("/api/product", tags = ["Consult"], response_model=list)
def findUsers(db: Session = Depends(get_db)):

        # Dades sensibles pes i preu

    buscar = select(product) # Buscamos todo en la base de datos
    result = db.exec(buscar).all() # Lo cojeremos todo, ya que en vez de coger first cogemos all
    comprovat = [] # Nueva lista para guardar cosas
    for persona in result: # Recorrera cada cosa que hayamos cogido en la consulta
        # Se añade a la lista cada objeto de la consulta
        comprovat.append(resposta.model_validate(persona)) # Pasamos que compruebe y lo metemos en la lista
    return comprovat # Devolvemos la lista
# Ex4
# Busca solament un atribut de tots els usuaris
@app.get("/api/product/{camp}", tags = ["Consult"], response_model=list[product])
def findUsers(camp: str , db: Session = Depends(get_db)):
    buscar = select(product).where(camp == product.name) # Filtramos el nombre que nos dara en el campo de name
    result = db.exec(buscar).all() # Cogemos todos los registros de ese campo
    return result # Devolvemos todos los registros que nos dan

# Ex5
# Elimina un usuari posan l'ID
@app.delete("/api/product/delete/{id}", tags = ["Remove"], response_model=dict)
def rmUsers(id: int , db: Session = Depends(get_db)):
    buscar = select(product).where(product.id == id) # Preparamos una consulta para poder filtrar por el ID
    result = db.exec(buscar).first() # Ejecutamos la consulta para que nos de 1 solo registro
    db.delete(result) # Eliminaremos el registro que nos da la consulta
    db.commit() # Guardamos cambios
    return {"msg":"L'eleminació ha sortit exitosament"} # Mensaje de respuesta positivo

# Ex6
# Busca tots els usuaris, eliminan les dades sensibles
@app.get("/api/productes3", tags = ["Consult"] , response_model=list)
def campsThreeUsers(db: Session = Depends(get_db)):
        # Dades sensibles pes i preu
    buscar = select(product) # Creamos una consulta basica para coger todos los registros
    result = db.exec(buscar).all() # Ejecutamos la consulta y hacemos que nos de TODOS los registros con ALL()
    comprovat = [] # Creamos una lista nueva para poder meter todos los reguistros
    for persona in result: # Recorremos todos los registros y los pasamos uno por uno
        # Se añade a la lista cada objeto de la consulta
        comprovat.append(respostaCorta.model_validate(persona)) # Añadimos cada registro de la lista en la lista con append, y le pasamos la plantilla de validate
    return comprovat # Devolvemos la lista completa con todos los resultados

# Ex7
# Actuliza un usuairo completo
@app.put("/api/actu/{id}", tags=["Actualitzacio"], response_model=dict)
def actuUser(id:int, user:Requisitos, db: Session = Depends(get_db)):
    actu = user.model_dump() # Convierte los parametros metidos como user en el modelo de Requisitos
    updt = ( # Parametizamos el comando para ponerlo en varias lineas
        update(product) # Primera instruccion, queremos actualizar
        .where(product.id == id) # Filtramos por el ID que hemos escogido
        .values(actu) # Actualizamos el usuario entero ya que no especificamos 1 solo campo
    ) # Instruccion para actualizar exactamente el usuario con el que nos pone le id
    db.exec(updt) # Ejecutamos el comando que tenemos que es la actualizacion
    db.commit() # Guardamos cambios
    return {"msg":"Usuari modificat correctament"} # Mensaje de respuesta positivo
# Ex 8
# Actualiza 1 sol camp d'un usuari
@app.patch("/api/actuName/{id}", tags=["Actualitzacio"], response_model=dict)
def actuNameUser(id:int, nameNew:str, db: Session = Depends(get_db)):
    updt = ( # Parametizamos el comando para ponerlo en varias lineas
        update(product) # Primera instruccion, queremos actualizar
        .where(product.id == id) # Filtramos por el ID que hemos escogido
        .values(name = nameNew) # Cambiamos el campo de Name por el nuevo campo
    ) # Instruccion para actualizar exactamente el nombre del usuario con el que nos pone el id
    db.exec(updt) # Ejecutamos la instruccion de actualizar
    db.commit() # Guardamos cambios
    return {"msg":"Nom modificat del user correctament"} # Mensaje de respuesta positivo
# Ex9
# Actualiza 2 camps d'un sol usuari
@app.patch("/api/actu2Camps/{id}", tags=["Actualitzacio"], response_model=dict)
def actuNameLastName(id:int, nameNew:str, lastnameNew:str, db: Session = Depends(get_db)):
    updt = ( # Parametizamos el comando para ponerlo en varias lineas
        update(product) # Primera instruccion, queremos actualizar
        .where(product.id == id) # Filtramos por el ID que hemos escogido
        .values(name = nameNew, lastname = lastnameNew) # Cambiamos los dos campos por los valores nuevos
    ) # Instruccion para actualizar exactamente el nombre y apellido del usuario con el que nos pone el id
    db.exec(updt) # Ejecutamos el comando de actualizar el usuario con sus campos correspondientes
    db.commit() # Guardamos cambios
    return {"msg":"Nom i cognom modificats del user correctament"} # Devolvemos mensaje con respuesta afirmativa