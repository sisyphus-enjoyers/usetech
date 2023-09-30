from sqlalchemy import Column, ForeignKey, Integer, String

from .database import Base


# class Log(Base):
    # __tablename__ = "logs"

    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String)
    # response_code = Column(Integer)
    # message = Column(String)
    # datetime = Column(DateTime)


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    host = Column(String)
    path = Column(String)


class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Policy(Base):
    __tablename__ = "policy"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    service_id = Column(Integer, ForeignKey("services.service_id"))