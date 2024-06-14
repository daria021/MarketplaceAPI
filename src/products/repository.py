from AbstractRepository import AbstractRepo
from .models import Product
from .schemas import ProductResponse, ProductUpdate, ProductCreate, ProductFilter


class ProductRepo(AbstractRepo):
    model = Product
    get_schema = ProductResponse
    update_schema = ProductUpdate
    create_schema = ProductCreate
    filter_schema = ProductFilter

    @classmethod
    async def validate(cls, obj: Product):
        await obj.awaitable_attrs.category
        return cls.get_schema.model_validate(obj)
