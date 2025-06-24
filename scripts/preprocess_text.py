# scripts/preprocess_text.py

import re
import json
import pandas as pd

def normalize_amharic_text(text):
    # Normalize common issues like weird spacing, English numbers, etc.
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'[፡።:]', ' ', text)  # Remove traditional Amharic punctuation
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces
    return text.strip()

def clean_data(input_json, output_csv):
    with open(input_json, encoding='utf-8') as f:
        raw_data = json.load(f)

    cleaned = []
    for item in raw_data:
        if not item.get('text'):
            continue
        cleaned.append({
            'channel': item['channel'],
            'message': normalize_amharic_text(item['text']),
            'timestamp': item['timestamp'],
            'views': item['views'],
            'image': item['image_url']
        })

    df = pd.DataFrame(cleaned)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ Saved cleaned data to {output_csv}")

if __name__ == "__main__":
    clean_data("data/raw/telegram_data.json", "data/processed/cleaned_messages.csv")
