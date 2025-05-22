# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.product import (  # noqa
    Product,
    Category,
    ProductImage,
    ProductSKU
)
from app.models.order import (  # noqa
    Order,
    OrderItem,
    OrderLog
)
from app.models.after_sale import (  # noqa
    AfterSale,
    AfterSaleItem,
    AfterSaleLog
)
from app.models.statistics import (  # noqa
    Statistics,
    SalesTrend,
    ProductRanking
) 