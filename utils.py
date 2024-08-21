import httpx
from bs4 import BeautifulSoup
from components.app_interface.configmanager import config



def get_data(link: str):
    try:
        resp = httpx.get(link)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            page_text = soup.get_text(separator=" ", strip=True)
            return page_text
        else:
            return f"Failed to retrieve the webpage: {resp.status_code}"
    except Exception as e:
        return e
    