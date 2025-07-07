import os
import re
import json

def build_index(data_dir = "data"):
    index = {}

    # Loop through each .txt file in the data folder
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            print(f"Indexing: {filepath}")
            with open(filepath, "r", encoding = "utf-8") as f:
                text = f.read()

            # Normalize text: Lowercase and split into words
            words = re.findall(r'\w+', text.lower())

            # Add each word to the index
            for word in words:
                if word not in index:
                    index[word] = []
                if filepath not in index[word]:
                    index[word].append(filepath)
            
    return index

if __name__ == "__main__":
    index = build_index("data")
    # Save index as JSON
    with open("index.json", "w", encoding = "utf-8") as f:
        json.dump(index, f, indent = 2)
    print("Indexing complete! Saved as index.json")