from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .models import DiscoveredFile

EXTS=( '.pdf','.zip','.rar','.7z','.jpg','.jpeg','.png','.mp4','.csv','.xlsx')

def discover_files(html:str, base_url:str)->list[DiscoveredFile]:
    soup=BeautifulSoup(html,'html.parser')
    results=[]
    for a in soup.find_all('a',href=True):
        href=a['href']
        if href.lower().endswith(EXTS):
            full=urljoin(base_url,href)
            results.append(DiscoveredFile(name=full.split('/')[-1],url=full))
    return results
