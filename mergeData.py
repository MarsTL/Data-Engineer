import json

with open('2901.json') as f1, open('2905.json') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)

combined = data1 + data2

with open('bcsample.json', 'w') as f:
    json.dump(combined, f, indent=2)

