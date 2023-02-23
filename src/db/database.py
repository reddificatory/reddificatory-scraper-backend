import psycopg2
import sys

sys.path.insert(0, 'D:\coding\python-reddit-tts\src')

import config

db = psycopg2.connect(database = config.DB_NAME,
                      host = config.DB_HOST,
                      user = config.DB_USER,
                      password = config.DB_PASS,
                      port = config.DB_PORT)

cursor = db.cursor()