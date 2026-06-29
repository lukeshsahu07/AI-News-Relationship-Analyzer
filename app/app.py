from flask import Flask, render_template, request
from api.news_fetcher import fetch_news
from ai.entity import extract_entities

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")

    articles = fetch_news(query)

    processed_articles = []

    graph_nodes = []
    graph_links = []

    for article in articles:
        title = article.get("title") or ""
        description = article.get("description") or ""

        text = title + " " + description

        entities = extract_entities(text)

        processed_articles.append({
            "title": title,
            "description": description,
            "url": article.get("url"),
            "urlToImage": article.get("urlToImage"),
            "entities": {
                "people": entities.get("people", []),
                "organizations": entities.get("organizations", []),
                "locations": entities.get("locations", [])
            }
        })

        # -------------------------
        # GRAPH BUILDING SECTION
        # -------------------------
        graph_nodes.append("News")

        for p in entities.get("people", []):
            graph_nodes.append(p)
            graph_links.append(("News", p))

        for o in entities.get("organizations", []):
            graph_nodes.append(o)
            graph_links.append(("News", o))

        for l in entities.get("locations", []):
            graph_nodes.append(l)
            graph_links.append(("News", l))

    return render_template(
        "results.html",
        articles=processed_articles,
        query=query,
        graph_nodes=list(set(graph_nodes)),
        graph_links=graph_links
    )


if __name__ == "__main__":
    app.run(debug=True)