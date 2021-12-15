from dotenv import load_dotenv
import json
import os
from pymongo import MongoClient
from .collections import db_clint

load_dotenv()
url = os.environ.get("MONGO_URL")
print(url)
client = MongoClient(url)

db = client[db_clint]

