from AbstractRepository import AbstractRepo
from category.models import Category
from category.schemas import CategoryUpdate, CategoryCreate, CategoryResponse, CategoryFilter


class CategoryRepo(AbstractRepo):
    model = Category
    get_schema = CategoryResponse
    update_schema = CategoryUpdate
    create_schema = CategoryCreate
    filter_schema = CategoryFilter
