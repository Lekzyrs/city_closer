from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class Waypoint(BaseModel):
    lat: float
    lng: float


class RoutingRequest(BaseModel):
    waypoints: List[Waypoint] = Field(..., min_length=2,
                                      description="Список точек маршрута [{lat, lng}]")


class NetworkType(str, Enum):
    """Тип транспортной сети"""
    DRIVE = "drive"
    WALK = "walk"
    BIKE = "bike"


class RouteResponse(BaseModel):
    """Модель ответа с GeoJSON"""
    type: str = "Feature"
    geometry: dict
    properties: dict


class ErrorResponse(BaseModel):
    """Модель ошибки"""
    error: str
    details: Optional[str] = None
    status_code: int
