from src.acquisition.clients.http_client import HttpClient
from .discovery import discover_files
from src.acquisition.models import AcquisitionResult

class AcquisitionService:
    def __init__(self):
        self.client=HttpClient()

    def analyse(self,url:str):
        response=self.client.get(url,timeout=30)
        ctype=response.headers.get('Content-Type','application/octet-stream')

        result=AcquisitionResult(
            source_url=url,
            final_url=response.url,
            status_code=response.status_code,
            content_type=ctype
        )

        if 'text/html' in ctype:
            result.discovered_files=discover_files(response.text,response.url)

        return result
