from fastapi import FastAPI

from category.routes import router as category_router
from products.routes import router as product_router

app = FastAPI(
    title="marketplaceAPI"
)

app.include_router(category_router)
app.include_router(product_router)
