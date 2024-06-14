from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, ConfigDict

from category.schemas import CategoryResponse
from .models import Product


class ProductUpdate(BaseModel):
    name: str
    description: str
    cost: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductUpdate):
    name: str
    description: str
    cost: int
    category_id: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    cost: int
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)


class ProductFilter(Filter):
    name__in: Optional[list[str]] = None
    description__like: Optional[str] = None
    cost__gte: Optional[int] = None
    cost__lte: Optional[int] = None

    class Constants(Filter.Constants):
        model = Product
