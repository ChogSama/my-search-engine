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
    
    # Save index as JSON
    with open("index.json", "w", encoding = "utf-8") as f:
        json.dump(index, f, indent = 2)
    print("Indexing complete! Saved as index.json")
    return index

def search(index, query):
    words = query.lower().split()
    if not words:
        print("No query entered.")
        return

    result_sets = []

    for word in words:
        if word in index:
            result_sets.append(set(index[word]))
        else:
            print(f"No results found for '{word}'.")
            return # Early exit if any word has no matches

    # Compute intersection of all result sets
    matching_files = set.intersection(*result_sets)

    if matching_files:
        print(f"Found pages containing all words: {', '.join(words)}")
        for filepath in matching_files:
            print(f"- {filepath}")
    else:
        print(f"No pages found containing all words: {', '.join(words)}")

if __name__ == "__main__":
    index = build_index("data")
    print("Starting search...")
    while True:
        query = input("Enter search term (or type 'exit' or 'reindex'): ").strip()
        if query.lower() == "exit":
            break
        elif query.lower() == "reindex":
            index = build_index("data")
            print("Reindexing complete!")
        else:
            search(index, query)