def extract_entities(text):
    text = (text or "").lower()

    people = []
    organizations = []
    locations = []

    if "elon musk" in text:
        people.append("Elon Musk")

    if "tesla" in text:
        organizations.append("Tesla")

    if "google" in text:
        organizations.append("Google")

    if "ai" in text or "artificial intelligence" in text:
        organizations.append("AI System")

    if "india" in text:
        locations.append("India")

    if "usa" in text or "united states" in text:
        locations.append("USA")

    return {
        "people": people,
        "organizations": organizations,
        "locations": locations
    }