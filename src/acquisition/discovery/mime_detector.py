def detect_content_type(response): return response.headers.get("Content-Type","application/octet-stream")
