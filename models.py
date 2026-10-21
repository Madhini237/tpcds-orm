from sqlalchemy.ext.automap import automap_base
from database import engine

Base = automap_base()

# Automatically map existing MySQL tables
Base.prepare(autoload_with=engine)

Customer = Base.classes.customer
StoreSales = Base.classes.store_sales
Item = Base.classes.item
DateDim = Base.classes.date_dim
Store = Base.classes.store

print("ORM models loaded successfully!")

print("\nCustomer columns:")
for column in Customer.__table__.columns:
    print(column.name, column.type)