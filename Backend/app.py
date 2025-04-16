from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)
CORS(app)  

client = MongoClient('mongodb://localhost:27017/')
db = client['zomato']
collection = db['restaurants']

def ensure_2dsphere_index():
    index_info = collection.index_information()
    if "location_2dsphere" not in index_info:
        collection.create_index([("location", "2dsphere")])
        print("2dsphere index created on the location field.")
    else:
        print("2dsphere index already exists.")

ensure_2dsphere_index()


@app.route('/restaurant/<restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    try:
        restaurant = collection.find_one({"Restaurant ID": int(restaurant_id)}, {'_id': 0})
        if restaurant:
            return jsonify(restaurant)
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid restaurant ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page
        restaurants = list(collection.find({}, {'_id': 0}).skip(skip).limit(per_page))
        return jsonify(restaurants)
    except ValueError:
        return jsonify({"error": "Invalid pagination parameters"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/restaurants/nearby', methods=['GET'])
def get_nearby_restaurants():
    try:
       
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 3)) * 1000  
        query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]  
                    },
                    "$maxDistance": radius
                }
            }
        }

        
        restaurants = list(collection.find(query, {'_id': 0}))
        if restaurants:
            return jsonify(restaurants)
        else:
            return jsonify({"message": "No restaurants found within the specified radius"}), 404
    except ValueError:
        return jsonify({"error": "Invalid latitude, longitude, or radius value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__== '__main__':
    app.run(debug=True)