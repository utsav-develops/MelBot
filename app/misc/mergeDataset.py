import json
import random

# ── Load all three datasets ─────────────────────────────────────────
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

whatsapp   = load('whatsapp_data.json')   # your 1500 pairs
toughlove  = load('tough_bro_training_data_500.json')  # AI generated 500
manual     = load('mel_training_data copy.json')  # original 30

# ── Sample whatsapp down to 700 ─────────────────────────────────────
random.shuffle(whatsapp)
whatsapp = whatsapp[:700]

# ── Merge all ───────────────────────────────────────────────────────
merged = whatsapp + toughlove + manual

# ── Shuffle so model doesn't learn order ────────────────────────────
random.shuffle(merged)

# ── Remove duplicates by input ──────────────────────────────────────
seen = set()
cleaned = []
for pair in merged:
    key = pair['input'].strip().lower()
    if key not in seen:
        seen.add(key)
        cleaned.append(pair)

# ── Save ─────────────────────────────────────────────────────────────
with open('mel_final_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f'WhatsApp pairs  : {len(whatsapp)}')
print(f'Tough love pairs: {len(toughlove)}')
print(f'Manual pairs    : {len(manual)}')
print(f'Total merged    : {len(merged)}')
print(f'After dedup     : {len(cleaned)}')
print(f'\n✅ Saved to mel_final_dataset.json')