import json


file = open("cameras.txt", "r")

list = []
for line in file.readlines():
    entities = line.split()
    obj ={}
    obj["id"] = entities[0]
    obj["latitude"] = entities[1]
    obj["longitude"] = entities[2]
    list.append(obj)
with open("cameras.json", "w") as to_write:
    json.dump(list, to_write, indent=4)