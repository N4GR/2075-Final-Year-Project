import sqlite3
import os

def run_startup():
    load_memory_database()

def load_memory_database(schema_location : str = "data/metaphrast-schema.txt"):
    # Load the queries from the txt.
    try:
        with open(schema_location, "r") as file:
            queries = [x.strip() for x in file.readlines()]
    
    except Exception as error:
        print(error)
        return False
    
    connection = sqlite3.connect("file:memb1?mode=memory&cache=shared", uri = True)
    cursor = connection.cursor()
    
    for query in queries:
        cursor.execute(query)
        connection.commit()