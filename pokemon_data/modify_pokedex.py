import json

with open("pokedex.json", encoding="utf-8") as pd_file:
    pd = json.load(pd_file)

for pokemon in pd:
    pokemon["Special"] = {
        "Attack": pokemon["Sp Attack"],
        "Defence": pokemon["Sp Defence"]
    }
    del pokemon["Sp Attack"]
    del pokemon["Sp Defence"]
print(pd[:10])

with open("pokedex.json", encoding="utf-8", mode="w") as pd_file:
    json.dump(pd, pd_file)
