def detect_content_type(response)->str:
    return response.headers.get('Content-Type','application/octet-stream')
