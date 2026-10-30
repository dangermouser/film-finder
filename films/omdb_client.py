import os
import requests

OMDB_URL = "https://www.omdbapi.com/"


class OmdbError(Exception):
    pass


def get_film(title, year):
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        raise OmdbError("OMDB_API_KEY is not set")

    params = {
        "apikey": api_key,
        "t": title,
        "y": year,
        "plot": "short",
        "r": "json",
    }

    try:
        response = requests.get(url=OMDB_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise OmdbError(f"Request failed: {e}") from e

    if data.get("Response") == "False":
        raise OmdbError(data.get("Error", "Film not found"))

    return data