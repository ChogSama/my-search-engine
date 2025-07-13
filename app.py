from flask import Flask, request, render_template_string
import os
import re
import json

app = Flask(__name__)

# Build index when server starts
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

index = build_index("data")

def search(index, query):
    words = query.lower().split()
    if not words:
        return []

    result_sets = []

    for word in words:
        if word in index:
            result_sets.append(set(index[word]))
        else:
            return [] # Early exit if any word not found

    # Compute intersection of all result sets
    matching_files = set.intersection(*result_sets)
    scored_results = []

    for filepath in matching_files:
        with open(filepath, "r", encoding = "utf-8") as f:
            text = f.read()

        score = sum(text.lower().count(word) for word in words)
        snippet = ""
        text_lower = text.lower()
        # Find first occurence of any query word
        for word in words:
            min_idx = min((text_lower.find(word) for word in words if text_lower.find(word) != -1), default = 0)
            start = max(0, min_idx - 30)
            end = min(len(text), min_idx + 60)
            snippet = text[start:end].replace("\n", " ").strip()

            # Highlight query words in this snippet
            for w in words:
                snippet = re.sub(f"(?i)({re.escape(w)})", r"<mark>\1</mark>", snippet)

        scored_results.append((filepath, snippet, score))

    scored_results.sort(key = lambda x: x[2], reverse = True)

    return [(filepath, snippets) for filepath, snippets, score in scored_results]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Mini Search Engine</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light text-dark">
        <div class="container mt-5">
            <div class="card shadow">
                <div class="card-body">
                    <h1 class="card-title text-center mb-4">Mini Search Engine</h1>
                    <form method="GET" class="d-flex mb-4">
                        <input type="text" name="q" class="form-control me-2" placeholder="Enter search query" value="{{query or ''}}" autofocus>
                        <button type="submit" class="btn btn-primary">Search</button>
                    </form>

                    {% if results is not none %}
                        <h3>Results for "<em>{{query}}</em>":</h3>
                        {% if results %}
                            <ul class="list-group">
                                {% for file, snippets in results %}
                                    <li class="list-group-item">
                                        <strong>{{file}}</strong>
                                        <ul class="mt-2>
                                            {% for snippet in snippets %}
                                                <li class="text-muted">{{snippet|safe}}</li>
                                            {% endfor %}
                                        </ul>
                                    </li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            <div class="alert alert-warning mt-3">No results found.</div>
                        {% endif %}
                    {% endif %}
                </div>
            </div>
        </div>
    </body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    query = request.args.get("q")
    results = None
    if query:
        results = search(index, query)
    return render_template_string(HTML_TEMPLATE, query = query, results = results)

if __name__ == "__main__":
    app.run(debug = True)