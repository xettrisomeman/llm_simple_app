from typing import List, Dict
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from urllib.parse import urlparse



SITE_TO_FORGET = [
    "www.youtube.com",
    "www.facebook.com",
    "www.quora.com",
    "www.twitter.com",
    "www.x.com",
    "www.reddit.com",
    "podcasts.hamropatro.com",
    "id-id.facebook.com",
    "da-dk.facebook.com",
    "th-th.facebook.com",
    "m.youtube.com",
    "m.facebook.com",
    "en.wikipedia.org"
]

ddg_search = DuckDuckGoSearchAPIWrapper()


def check_domain(url: str, exclude_urls: list) -> bool:
    domain = urlparse(url).netloc
    return domain in exclude_urls

def web_search(query: str, num_results: int, timelimit: str) -> List[Dict[str, str]]:
    ddg_search.time = timelimit
    results = ddg_search.results(query, max_results=50)
    without_youtube_and_reddit = []
    for links in results:
        if not check_domain(links['link'], SITE_TO_FORGET):
            without_youtube_and_reddit.append(links)
    return without_youtube_and_reddit[:num_results]
