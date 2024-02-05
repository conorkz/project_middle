from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from fastapi.openapi.models import HTTPBaseModel
from fastapi.openapi.models import Model
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "database_url"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    points = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class Point(BaseModel):
    lat: float
    lng: float

class RouteCreate(BaseModel):
    points: List[Point]

class RouteResponse(BaseModel):
    id: int
    points: List[Point]

@app.post("/api/routes", response_model=RouteResponse)
async def create_route(route_create: RouteCreate, format: str = Query(None)):
    start_point = route_create.points[0]
    route = Route(points=str(route_create.points))
    db = SessionLocal()
    db.add(route)
    db.commit()
    db.refresh(route)
    db.close()
    return route

@app.get("/api/routes/{id}", response_model=RouteResponse)
async def get_route(id: int):
    db = SessionLocal()
    route = db.query(Route).filter(Route.id == id).first()
    db.close()
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    points = eval(route.points)
    return {"id": route.id, "points": points}

