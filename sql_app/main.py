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
    if not db_service:
        raise HTTPException(status_code=400, detail="Service already registered")
    return crud.create_service(db=db, service=service)


@app.get("/access/", response_model=schemas.Policy)
def is_get_service_access(client_id: int, service_id: int, db: Session = Depends(get_db)):
    access = crud.if_client_access_service(db, client_id=client_id, service_id=service_id)
    if access:
        return access
    raise HTTPException(status_code=400, detail="Service doesn`t exist")


@app.post("/policy/", response_model=schemas.Policy)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, policy.client_id)
    db_service = crud.get_service(db, policy.service_id)
    if not db_client or not db_service:
        raise HTTPException(status_code=400, detail="User or service doesn`t exist")
    return crud.add_policy(db=db, policy=policy)