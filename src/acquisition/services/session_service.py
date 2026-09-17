import requests
def create_session():
 s=requests.Session(); s.headers.update({"User-Agent":"Hash-Link/1.2"}); return s
