import requests
from difflib import get_close_matches

SERPAPI_KEY = "Your_api_key"

def search_web(query):
    url = "https://serpapi.com/search"
    params = {
        "q":query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return "Bot: Hmm, I couldn't connect to the search service right now."

        data = response.json()
        results = []

        organic = data.get("organic_results")
        if organic:
            for result in organic[:3]:  # Top 3 results
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                link = result.get("link", "")
                results.append(f"- {title}: {snippet}\n{link}")
            return "\n\n".join(results)
        else:
            return "Bot: Sorry, I couldn’t find any useful search results for that."

    except requests.exceptions.RequestException:
        return "Bot: Something went wrong while trying to search the web. Please try again later."

site_urls = {
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "linkedin": "https://www.linkedin.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "gmail": "https://mail.google.com",
    "twitter": "https://www.twitter.com",
    "myntra": "https://www.myntra.com",
}

def extract_site_name(user_prompt):
    user_prompt = user_prompt.lower()
    site_names = list(site_urls.keys())

    for site in site_names:
        if site in user_prompt:
            return site

    # Fuzzy match (typos like "flipkar" ≈ "flipkart")
    close = get_close_matches(user_prompt, site_names, n=1, cutoff=0.8)
    return close[0] if close else None
