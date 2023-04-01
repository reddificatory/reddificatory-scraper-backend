import os
import sys
sys.path.insert(0, os.getcwd() + '/src')

import psycopg2
import config

database = psycopg2.connect(database = config.DB_NAME,
                      host = config.DB_HOST,
                      user = config.DB_USER,
                      password = config.DB_PASS,
                      port = config.DB_PORT)

cursor = database.cursor()