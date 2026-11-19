import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def get_config(key):
    return os.getenv(key) or st.secrets.get(key)

DB_HOST = get_config("DB_HOST")
DB_PORT = get_config("DB_PORT")
DB_NAME = get_config("DB_NAME")
DB_USER = get_config("DB_USER")
DB_PASSWORD = get_config("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT version()")
            )

            print("Database connected successfully!")
            print(result.scalar())

    except Exception as error:
        print("Database connection failed:", error)


if __name__ == "__main__":
    test_connection()
