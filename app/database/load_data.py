import pandas as pd
from app.database.connection import engine

tables = {
    "orders": "data/cleaned/orders_cleaned.csv",
    "customers": "data/cleaned/customers_cleaned.csv",
    "payments": "data/cleaned/payments_cleaned.csv",
    "orderitems": "data/cleaned/orderitems_cleaned.csv",
    "products": "data/cleaned/products_cleaned.csv",
    "reviews": "data/cleaned/reviews_cleaned.csv",
    "sellers": "data/cleaned/sellers_cleaned.csv",
    "categories": "data/cleaned/categories_cleaned.csv",
    "geolocation": "data/cleaned/geolocation_cleaned.csv",
}

for table_name, file_path in tables.items():
    print(f"Loading {table_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=500,
        method="multi"
    )

    print(f"{table_name} uploaded.")

print("All tables uploaded successfully!")