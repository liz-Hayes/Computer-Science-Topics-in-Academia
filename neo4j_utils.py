from neo4j import GraphDatabase
import pandas as pd

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "test_root")
DATABASE = "academicworld"
    

def query(q, uri=URI, auth=AUTH, db=DATABASE):
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        records, summary, keys = driver.execute_query(q,database_=db)
    return pd.DataFrame(records)



