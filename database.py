
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

load_dotenv()

url = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "tpcds"),
)

engine = create_engine(url, pool_pre_ping=True)

if __name__ == "__main__":
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        )
        print("Connected successfully:", result.fetchone())
