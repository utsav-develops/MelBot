import json

with open('merged_chat_dataset.json', 'r') as f:
    data = json.load(f)

# Basic stats
lengths = [len(x['output'].split()) for x in data]
print(f"Total pairs: {len(data)}")
print(f"Avg output length: {sum(lengths)/len(lengths):.1f} words")
print(f"Short outputs (<3 words): {sum(1 for l in lengths if l < 3)}")
print(f"Very long outputs (>50 words): {sum(1 for l in lengths if l > 50)}")

# Sample 5 random pairs
import random
for x in random.sample(data, 5):
    print(f"\nIN:  {x['input']}")
    print(f"OUT: {x['output']}")