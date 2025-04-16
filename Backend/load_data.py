import pandas as pd
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['zomato']
collection = db['restaurants']

# Load JSON files
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Load CSV files
def load_csv(file_path):
    return pd.read_csv(file_path)

# Load JSON data
json_files = [
    r'C:\zomato-clone\data\file1.json',
    r'C:\zomato-clone\data\file2.json',
    r'C:\zomato-clone\data\file3.json',
    r'C:\zomato-clone\data\file4.json',
    r'C:\zomato-clone\data\file5.json'
]

for file in json_files:
    data = load_json(file)
    collection.insert_many(data)

# Load CSV data
zomato_df = load_csv(r'C:\zomato-clone\data\zomato.csv')
country_code_df = load_csv(r'C:\zomato-clone\data\Country-Code.csv')

# Insert CSV data into MongoDB
collection.insert_many(zomato_df.to_dict('records'))
collection.insert_many(country_code_df.to_dict('records'))

print("Data loaded into MongoDB successfully!")