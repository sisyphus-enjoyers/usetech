from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    

class ClientCreate(ClientBase):
    name: str


class Client(ClientBase):
    client_id: int
    name: str

    class Config:
        orm_mode = True



class ServiceBase(BaseModel):
    name: str
    

class ServiceCreate(ServiceBase):
    name: str
    host: str
    path: str


class Service(ServiceBase):
    service_id: int
    name: str
    host: str
    path: str


    class Config:
        orm_mode = True
