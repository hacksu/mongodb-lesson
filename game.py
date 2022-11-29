from random import randrange
from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint

client = MongoClient(
    host="mitch.website",
    username="student",
    password="[[[password]]]"
)
db = client.pokemon
collection = db.PC

id_query = {"_id": ObjectId("my thing")}
my_pokemon = collection.find_one(id_query)
while my_pokemon["hp"] > 0 and my_pokemon["xp"] < 100:
    print("Your pokemon:")
    pprint(my_pokemon)
    available_pokemon = collection.count_documents({})
    random_pokemon = collection.find({})[randrange(0, available_pokemon)]
    print(f"A wild pokemon appeared!")
    pprint(random_pokemon)
    decision = input("fight or flee?")
    if decision == "fight":
        collection.update_one(id_query, {"$inc": {"hp": randrange(-5, 0)}})
        collection.update_one(id_query, {"$inc": {"xp": randrange(5, 10)}})
    else:
        collection.update_one(
            {"_id": random_pokemon["id"]},
            {"$inc": {"xp": randrange(5, 10)}}
        )
if my_pokemon["hp"] <= 0:
    print("you lost! insert a new pokemon to try again")
elif my_pokemon["xp"] > 100:
    print("your pokemon wins!")
print("the final state of your pokemon:")
pprint(collection.find_one(id_query))
