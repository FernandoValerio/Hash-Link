def build_manifest_fragment(url:str, hashes:dict|None=None)->dict:
    return {'source_url':url,'hashes':hashes or {}}
