import json

with open('faq_0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

for i, chunk in enumerate([data[x:x+200] for x in range(0, len(data), 200)]):
    with open(f'faq_0_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)

with open('faq_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

for i, chunk in enumerate([data[x:x+200] for x in range(0, len(data), 200)]):
    with open(f'faq_1_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)
