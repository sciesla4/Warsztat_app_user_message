# Let's check if database app_wartsztat exist, if not create database
from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

CREATE_DB_NAME = "CREATE DATABASE workshop;"

CREATE_USERS = """CREATE TABLE users(
               id serial,
               username varchar(255) UNIQUE ,
               hashed_password varchar(80),
               PRIMARY KEY(id));"""

CREATE_MESSAGES = """CREATE TABLE messages(
               id serial,
               from_id int ,
               to_id int ,
               text varchar(255),
               creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY(from_id) references users(id) ON DELETE CASCADE,
               FOREIGN KEY(to_id) references users(id) ON DELETE CASCADE
               );"""

DB_USER = "postgres"
DB_PASS = "coderslab"
DB_HOST = "localhost"
DB_NAME = "workshop"

try:
    con = connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
    con.autocommit = True
    try:
        cur = con.cursor()
        cur.execute(CREATE_DB_NAME)

    except DuplicateDatabase as e:
        print("Database exist", e)

    con.close()

except OperationalError as e:
    print("Connection error", e)

try:
    con = connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    con.autocommit = True
    cur = con.cursor()
    try:
        cur.execute(CREATE_USERS)
    except DuplicateTable as e:
        print("Table exist", e)

    try:
        cur.execute(CREATE_MESSAGES)
    except DuplicateTable as e:
        print("Table exist", e)

    con.close()

except OperationalError as e:
    print("Connection error", e)
