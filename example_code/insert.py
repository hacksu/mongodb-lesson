from pymongo import MongoClient

client = MongoClient(
    host="mitch.website",
    username="student",
    password="bowman218"
)
db = client.pokemon
collection = db.PC

result = collection.insert_one({
  "name": "Squinchy",
  "species": "Wartortle",
  "hp": 100,   # important
  "xp": 0,     # important
  "mood": "bemused"
})
print(result.inserted_id)
