from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum


class RoutingRequest(BaseModel):
    """Модель запроса на построение маршрута"""
    ids: List[int] = Field(..., min_items=2,
                           description="Массив ID киосков (OSM node IDs)")

    @validator('ids')
    def check_unique_ids(cls, v):
        """Проверяем, что ID уникальны (опционально)"""
        if len(v) != len(set(v)):
            pass
        return v


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
