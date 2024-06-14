from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import NotFoundException
from .models import Category
from .repository import CategoryRepo
from .schemas import CategoryResponse, CategoryCreate, CategoryUpdate, CategoryFilter
from database import get_async_session

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.post("")
async def create_category(
        category: CategoryCreate,
        session: AsyncSession = Depends(get_async_session)) -> CategoryResponse:
    category = await CategoryRepo.create(session=session, **category.model_dump())
    return category


@router.get("/{category_id}")
async def get_one_category(category_id: int, session: AsyncSession = Depends(get_async_session)) -> CategoryResponse:
    try:
        res = await CategoryRepo.get(record_id=category_id, session=session)
    except NotFoundException:
        raise HTTPException(404, "No category found")
    return res


@router.get("")
async def get_all_categories(
        session: AsyncSession = Depends(get_async_session)
) -> list[CategoryResponse]:
    res = await CategoryRepo.get_all(session=session)
    return res


filter_router = APIRouter(
    prefix="/filter"
)


@filter_router.get("/")
async def get_filter_category(
        filters: CategoryFilter = FilterDepends(CategoryFilter),
        session: AsyncSession = Depends(get_async_session)
) -> list[CategoryResponse]:
    res = await CategoryRepo.get_filtered_by(session=session, filter=filters)
    return res


router.include_router(filter_router)


@router.put("/{category_id}")
async def update_category(
        category_id: int,
        update: CategoryUpdate,
        session: AsyncSession = Depends(get_async_session)) -> CategoryResponse:
    try:
        category = await CategoryRepo.update(record_id=category_id, session=session, **update.model_dump())
    except NotFoundException:
        raise HTTPException(404, "No category found")
    return category


@router.delete("/{category_id}")
async def delete_category(category_id: int,
                          session: AsyncSession = Depends(get_async_session)) -> None:
    await CategoryRepo.delete(record_id=category_id, session=session)
