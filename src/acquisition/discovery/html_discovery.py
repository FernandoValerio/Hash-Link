from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.acquisition.models.discovered_file import DiscoveredFile

def discover(html,base_url):
    res=[]; soup=BeautifulSoup(html,"html.parser")
    for a in soup.find_all("a",href=True):
         res.append(
              DiscoveredFile(
                   name=a.get_text(strip=True),
                   url=urljoin(base_url, a["href"])
              )
         )
    return res
