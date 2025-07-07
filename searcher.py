import json

def load_index(index_file = "index.json"):
    with open(index_file, "r", encoding = "utf-8") as f:
        return json.load(f)

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
    index = load_index("index.json")
    while True:
        query = input("Enter search term (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        search(index, query)
