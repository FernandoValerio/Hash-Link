from PyPDF2 import PdfReader

from .metadata_info import MetadataInfo


class PdfMetadata:

    @staticmethod
    def extract(path):

        reader = PdfReader(path)

        meta = reader.metadata or {}

        summary = {
            "Autor": str(meta.get("/Author", "")),
            "Criador": str(meta.get("/Creator", "")),
            "Páginas": len(reader.pages),
        }

        full_data = {}

        for key, value in meta.items():
            full_data[str(key)] = str(value)

        full_data["Pages"] = len(
            reader.pages
        )

        return MetadataInfo(
            file_type="PDF",
            summary=summary,
            full_data=full_data
        )