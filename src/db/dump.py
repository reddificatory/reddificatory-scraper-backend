import config
import psycopg2
from database import db

cursor = db.cursor()

def create_tables():
    tables = [
        """
            CREATE TABLE IF NOT EXISTS submissions (
                "submission_id" VARCHAR ( 16 ) UNIQUE NOT NULL PRIMARY KEY,
                "used" BOOLEAN DEFAULT FALSE,
                "created_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp),
                "updated_at" TIMESTAMP NOT NULL DEFAULT (current_timestamp)
            );
        """
    ]

    for table in tables:
        print(table)

print(db)
print(cursor)
print(create_tables())