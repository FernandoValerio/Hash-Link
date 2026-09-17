from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .models import DiscoveredFile

DISCOVERABLE=(".pdf",".zip",".rar",".7z",".jpg",".jpeg",".png",".mp4",".csv",".xlsx")

def discover_files(html:str,base_url:str):
    soup=BeautifulSoup(html,"html.parser")
    results=[]
    for a in soup.find_all('a',href=True):
        href=a['href']
        if href.lower().endswith(DISCOVERABLE):
            results.append(DiscoveredFile(name=href.split('/')[-1],url=urljoin(base_url,href)))
    return results
