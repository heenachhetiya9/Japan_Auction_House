from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = "mysql+pymysql://root:admin%40123@localhost:3306/japan_auction_house"

engine = create_engine(DATABASE_URL)
# print("Database connection established successfully!")
