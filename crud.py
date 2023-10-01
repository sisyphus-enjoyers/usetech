from sqlalchemy.orm import Session

import models
import schemas


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.client_id == client_id).first()

def get_all_clients(db: Session):
    return db.query(models.Client)

def get_client_by_name(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(name=client.name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.service_id == service_id).first()

def get_all_services(db: Session):
    return db.query(models.Service)

def if_service_exist(db: Session, name: str, host: str, path: str):
    return db.query(models.Service).filter(models.Service.name == name or (models.Service.host == host and models.Service.path == path)).first()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(name=service.name, host=service.host, path=service.path)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_client_services(db: Session, client_id: int):
    return db.query(models.Policy).filter(models.Policy.client_id == client_id)

def if_client_access_service(db: Session, client_id: int, service_id: int):
    return db.query(models.Policy).filter(models.Policy.client_id == client_id, models.Policy.service_id == service_id).first()
    

def add_policy(db: Session, policy: schemas.PolicyCreate):
    db_policy = models.Policy(client_id=policy.client_id, service_id=policy.service_id)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy
