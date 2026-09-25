from pathlib import Path
from datetime import datetime

from .metadata_info import MetadataInfo


class GenericMetadata:

    @staticmethod
    def extract(path):

        path = Path(path)

        stat = path.stat()

        summary = {
            "Tipo": path.suffix.upper(),
            "Tamanho": f"{stat.st_size:,} bytes",
        }

        full_data = {
            "Nome": path.name,
            "Caminho": str(path),
            "Extensão": path.suffix,
            "Tamanho": stat.st_size,
            "Criado": datetime.fromtimestamp(
                stat.st_ctime
            ).strftime("%d/%m/%Y %H:%M:%S"),
            "Modificado": datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%d/%m/%Y %H:%M:%S"),
        }

        return MetadataInfo(
            file_type="Arquivo",
            summary=summary,
            full_data=full_data
        )