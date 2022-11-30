from pymongo import MongoClient

client = MongoClient("your config")

pokemon = client.pokemon
pokedex = pokemon.pokedex
PC = pokemon.PC

print(pokedex.find_one({}))

try:
    print(pokedex.delete_one({}))
except Exception as e:
    print("good that didn't work")
    print(e)
    print()

try:
    print(pokedex.insert_one({"thing": "lol"}))
except Exception as e:
    print("good that didn't work")
    print(e)
    print()

result = PC.insert_one({
    "name": "squinchy",
    "species": "Wartortle",
    "HP": 45,
    "mood": "Bemused"
})

id = result.inserted_id
print("inserted", id)
print()

try:
    print(PC.delete_one({}))
except Exception as e:
    print("good that didn't work")
    print(e)
    print()

PC.update_one({
    "_id": id,
}, {
    "$set": {"owner": "Mitch"}
})

print(PC.find_one({"_id": id}))
