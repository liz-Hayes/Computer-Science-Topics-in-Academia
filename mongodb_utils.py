from pymongo import MongoClient
import pandas as pd

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1"
DATABASE = "academicworld"

def connect(connection_string=CONNECTION_STRING,database_name=DATABASE):
   client = MongoClient(connection_string)
   return client[database_name]

def query(collection,agg_pipeline):
    dbname = connect()
    collection_name = dbname[collection]
    query_result = collection_name.aggregate(agg_pipeline)
    return pd.DataFrame(query_result)

def insert(collection,item):
    dbname = connect()
    collection_name = dbname[collection]
    collection_name.insert_one(item)

def delete(collection,q):
    dbname = connect()
    collection_name = dbname[collection]
    collection_name.delete_one(q)
    
    