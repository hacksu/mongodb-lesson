from pprint import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from random import randrange

client = MongoClient("your config")
db = client.pokemon
collection = db.PC

my_id = ObjectId("your id")
id_query = { "_id": my_id }

my_pokemon = collection.find_one(id_query)
pprint(my_pokemon)

if my_pokemon["hp"] <= 0:
    print("you lose :(")
elif my_pokemon["xp"] > 100:
    print("you win! :)")
else:
    available_pokemon = collection.count_documents({})
    random_index = randrange(0, available_pokemon)
    random_pokemon = collection.find({})[random_index]
    print("A wild pokemon appeared!")
    pprint(random_pokemon)
    if "xp" in random_pokemon or "hp" in random_pokemon:
        decision = input("fight or flee? ")
        if decision == "fight":
            hp_decrease = -randrange(0, 5)
            xp_increase = randrange(5, 10)
            collection.update_one(
                id_query,
                {"$inc": {"hp": hp_decrease}}
            )
            collection.update_one(
                id_query,
                {"$inc": {"xp": xp_increase}}
            )
        else:
            collection.update_one(
                {"_id": random_pokemon["_id"]},
                {"$inc": {"xp": randrange(5, 10)}}
            )
print("your pokemon")
pprint(collection.find_one(id_query))

# improvements: we also could make sure that the random pokemon isn't your
# pokemon
