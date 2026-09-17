from datetime import datetime

class ManifestBuilder:
    def build(self, acquisition_id, source_url, final_url, algorithms, files):
        return {
            "acquisition_id": acquisition_id,
            "source_url": source_url,
            "final_url": final_url,
            "started_at": datetime.now().isoformat(),
            "algorithms": algorithms,
            "files": files,
        }
