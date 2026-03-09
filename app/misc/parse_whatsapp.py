import re
import json
import sys

YOUR_NAME = "Utsav Acharya"
INPUT_FILE = "_chat.txt"       
OUTPUT_FILE = "mel_training_data.json"
MIN_LENGTH = 2
MAX_LENGTH = 200              

pattern = re.compile(r'\[(\d+/\d+/\d+), (\d+:\d+:\d+)\] ([^:]+): (.+)')

messages =[]

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        match = pattern.match(line.strip())
        if match:
            _, _, sender, text = match.groups()
            # skip system messages
            if text in ['<Media omitted>', 'This message was deleted', 'null']:
                continue
            messages.append({
                'sender': sender.strip(),
                'text': text.strip()
            })

pairs = []

for i in range(1, len(messages)):
    prev = messages[i - 1]
    curr = messages[i]

    # current message is Utsav's reply to someone else
    if curr['sender'] == YOUR_NAME and prev['sender'] != YOUR_NAME:
        input_text = prev['text']
        output_text = curr['text']

        # filter noise
        if (MIN_LENGTH <= len(output_text) <= MAX_LENGTH and
            MIN_LENGTH <= len(input_text) <= MAX_LENGTH):
            pairs.append({
                "input": input_text.lower(),
                "output": output_text
            })

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(pairs, f, ensure_ascii=False, indent=2)

print(f'✅ Done — {len(pairs)} training pairs saved to {OUTPUT_FILE}')
print(f'\nSample:')
for p in pairs[:5]:
    print(f'  IN:  {p["input"]}')
    print(f'  OUT: {p["output"]}')
    print()