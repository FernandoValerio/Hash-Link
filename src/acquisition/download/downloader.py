from pathlib import Path
class Downloader:
 def download(self,session,url,destination,callback=None):
  p=Path(destination)
  with session.get(url,stream=True) as r:
   total=int(r.headers.get("Content-Length",0)); got=0
   with open(p,"wb") as f:
    for c in r.iter_content(1024*1024):
      if c: f.write(c); got+=len(c); callback and callback(got,total)
  return p
