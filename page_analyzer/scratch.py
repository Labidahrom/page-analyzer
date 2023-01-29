import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute("SELECT * FROM urls ORDER BY id DESC")
database = cursor.fetchall()
print(database)


