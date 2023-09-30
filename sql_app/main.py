from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/clients/{client_id}", response_model=schemas.Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id=client_id)
    if client:
        return client
    raise HTTPException(status_code=400, detail="Client doesn`t exist")

@app.get("/clients/", response_model=list[schemas.Client])
def get_clients(db: Session = Depends(get_db)):
    clients = crud.get_all_clients(db)
    return clients


@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_name(db, name=client.name)
    if db_client:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_client(db=db, client=client)



@app.get("/services/{service_id}", response_model=schemas.Service)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = crud.get_service(db, service_id=service_id)
    if service:
        return service
    raise HTTPException(status_code=400, detail="Service doesn`t exist")
    

@app.get("/services/", response_model=list[schemas.Service])
def get_services(db: Session = Depends(get_db)):
    services = crud.get_all_services(db)
    return services


@app.post("/services/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = crud.if_service_exist(db, name=service.name, host=service.host, path=service.path)
    if db_service:
        raise HTTPException(status_code=400, detail="Service already registered")
    return crud.create_service(db=db, service=service)


