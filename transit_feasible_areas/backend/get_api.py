import json
import httpx
import os
from pathlib import Path
import re

START_URL_ISOLINES = "https://api.geoapify.com/v1/isoline?"
START_URL_PLACES = "https://api.geoapify.com/v2/places?"
IGNORED_KEYS = ["api_key","apikey"]
ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyz1234567890%+,^=_"
CACHE_DIR = Path(__file__).parent/ "data/cached"


try:
    API_KEY = os.getenv("API_KEY")
except KeyError:
    raise Exception(
        "Make sure that you have set the API Key environment variable."
    )


class RequestException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )


def combine_url_with_params(url, params):
    """
    Use httpx.URL to create a URL joined to its parameters, suitable for use
    for cache keys.

    Parameters:
        - url: a URL with or without parameters already
        - params: a dictionary of parameters to add

    Returns:
        The URL with parameters added, for example:

    """
    url = httpx.URL(url)
    params = dict(url.params) | params 
    return str(url.copy_with(params=params))

def url_to_cache_key(url: str) -> str:
    """
    Convert a URL to a cache key that can be stored on disk.

    This lets us administer unique filenames per request.
    """
    url_pivot = url.lower().removeprefix("https://")
    cache_key = re.sub(f"[^{re.escape(ALLOWED_CHARS)}]", "_", url_pivot)

    return cache_key


def cached_get(url, kwargs) -> dict:
    """
    This function caches all GET requests it makes, by writing
    the successful responses to disk.

    When creating the cache_key this function must
    include all parameters EXCEPT those included in config.IGNORED_KEYS.

    This is to avoid writing your API key to disk hundreds of times.
    A potential security risk if someone were to see those files somehow.

    Parameters:
        url:        Base URL to visit.
        **kwargs:   Keyword-arguments that will be appended to the URL as
                    query parameters.

    Returns:
        Contents of response as text.

    Raises:
        FetchException if a non-200 response occurs.
    """
    query_url = combine_url_with_params(url, kwargs)
    file_params = {k: v for k, v in kwargs.items() if k not in IGNORED_KEYS}
    cached_key = url_to_cache_key(combine_url_with_params(url, file_params))
    cached_key_path = CACHE_DIR / cached_key

    # Case 1. The URL is already in the cache.
    if cached_key_path.exists():
        return cached_key_path.read_text()

    response = httpx.get(query_url, follow_redirects=True)
    if response.status_code == 200:
        # Case 2. The URL is not in the cache, and server responds with a 200 OK.
        CACHE_DIR.mkdir(exist_ok=True, parents=True)
        cached_key_path.write_text(response.text)
        return response.text
    else:
        # Case 3. The URL is not in the cache, and the server responds an error.
        raise RequestException(response)
    


def get_distance(lon, lat, mode, range):
    """"
    Use cached_get to retrieve isocrone time
    Input: 
        lon
        lat
        range - time available to 
        mode - vehicle in which the person is moving
    Output:
        isoline
    """
    kwargs = {"type": "time",
              "lon": lon,
              "lat": lat,
              "mode": mode,
              "range": range,
              "avoid": "ferries|highways",
              "traffic": "approximated",
              "api_key": API_KEY
                }
    return json.loads(cached_get(START_URL_ISOLINES, kwargs))
  

def get_points(geometry_id, lon, lat):
    """"
    Use cached_get to retrieve isocrone time
    Input: 
        geometry

    Output:
        list of Points
    """
    kwargs = {"categories": "catering.cafe,education.library,catering.bar,sport.sports_centre",
              "filter": f"geometry:{geometry_id}",
              "bias": f"proximity:{lon},{lat}",
              "limit": 50,
              "api_key": API_KEY
                }
    
    return json.loads(cached_get(START_URL_PLACES, kwargs))
