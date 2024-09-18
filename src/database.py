import json

database="database.json"

with open(database,"r") as f:
    data=json.load(f)

print(data["1234"]["Citizenship"]["year_of_birth"])
    