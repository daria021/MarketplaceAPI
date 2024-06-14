from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel
from pydantic import ConfigDict

from .models import Category


class CategoryUpdate(BaseModel):
    name: str
    description: str
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(CategoryUpdate):
    name: str
    description: str


class CategoryResponse(CategoryCreate):
    id: int
    name: str
    description: str


class CategoryFilter(Filter):
    name__in: Optional[list[str]] = None
    description__like: Optional[str] = None

    class Constants(Filter.Constants):
        model = Category
