from pymongo import MongoClient  # Import the MongoDB client

# Step 1: Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Connect to the local MongoDB server
db = client['zomato']  # Access the 'zomato' database
collection = db['restaurants']  # Access the 'restaurants' collection

# Step 2: Function to update all documents
def update_location_field():
    for doc in collection.find():  # Loop through all documents in the collection
        if "Longitude" in doc and "Latitude" in doc:  # Check if longitude and latitude exist
            lon, lat = doc["Longitude"], doc["Latitude"]  # Extract values
            collection.update_one(  # Update the document
                {"_id": doc["_id"]},  # Filter by the document's unique ID
                {"$set": {  # Add the 'location' field
                    "location": {
                        "type": "Point",  # Specify GeoJSON type
                        "coordinates": [lon, lat]  # Set GeoJSON coordinates [longitude, latitude]
                    }
                }}
            )
    print("Updated all documents with GeoJSON location format.")

# Step 3: Run the function
update_location_field()