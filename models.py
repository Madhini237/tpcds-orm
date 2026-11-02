from sqlalchemy.ext.automap import automap_base
from database import engine

# Create the automap base
Base = automap_base()

# Automatically load models from the existing database tables
Base.prepare(autoload_with=engine)

# Map existing TPC-DS tables
Customer = Base.classes.customer
StoreSales = Base.classes.store_sales
Item = Base.classes.item
DateDim = Base.classes.date_dim
Store = Base.classes.store

print("ORM models loaded successfully!")

# Display customer columns to verify mapping
print("Customer columns:", Customer.__table__.columns.keys())

# Display date_dim columns to verify mapping
print("DateDim columns:", DateDim.__table__.columns.keys())
