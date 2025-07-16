from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

DB_CONFIG = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)