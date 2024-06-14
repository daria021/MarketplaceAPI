from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from exceptions import NotFoundException
from .models import Product
from .repository import ProductRepo
from .schemas import ProductResponse, ProductCreate, ProductUpdate, ProductFilter

router = APIRouter(
    prefix="/product",
    tags=["product/"],
)


@router.post("")
async def create_product(product: ProductCreate,
                         session: AsyncSession = Depends(get_async_session)) -> ProductResponse:
    product = await ProductRepo.create(session=session, **product.model_dump())
    return product


@router.get("/{product_id}")
async def get_one_product(product_id: int, session: AsyncSession = Depends(get_async_session)) -> ProductResponse:
    try:
        res = await ProductRepo.get(record_id=product_id, session=session)
    except NotFoundException:
        raise HTTPException(404, "No category found")
    return res


@router.get("/")
async def get_all_products(
        session: AsyncSession = Depends(get_async_session)
) -> list[ProductResponse]:
    res = await ProductRepo.get_all(session=session)
    return res


filter_router = APIRouter(
    prefix="/filter"
)


@filter_router.get("/")
async def get_filter_products(
        filters: ProductFilter = FilterDepends(ProductFilter),
        session: AsyncSession = Depends(get_async_session)
) -> list[ProductResponse]:
    res = await ProductRepo.get_filtered_by(session=session, filter=filters)
    return res


router.include_router(filter_router)


@router.put("/{product_id}")
async def update_product(
        product_id: int,
        update: ProductUpdate,
        session: AsyncSession = Depends(get_async_session)) -> ProductResponse:
    try:
        product = await ProductRepo.update(record_id=product_id, session=session, **update.model_dump())
    except NotFoundException:
        raise HTTPException(404, "No category found")
    return product


@router.delete("{product_id}")
async def delete_product(product_id: int,
                         session: AsyncSession = Depends(get_async_session)) -> None:
    await ProductRepo.delete(record_id=product_id, session=session)
