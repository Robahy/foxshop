from .customer import router as customer_router
from .factor import router as factor_router
from .personnel import router as personnel_router
from .product import router as product_router

__all__ = (
    "customer_router",
    "factor_router",
    "personnel_router",
    "product_router"
)