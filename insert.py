from pymongo import MongoClient

client = MongoClient(
    host="mitch.website",
    username="student",
    password="[[password...]]"
)
db = client.pokemon
collection = db.PC

result = collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "current_hp": 10,
  "mood": "bemused"
})
print(result.inserted_id)
