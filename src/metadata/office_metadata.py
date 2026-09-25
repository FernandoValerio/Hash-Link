from pathlib import Path

from docx import Document
from openpyxl import load_workbook

from .metadata_info import MetadataInfo


class OfficeMetadata:

    @staticmethod
    def extract(path):

        path = Path(path)

        ext = path.suffix.lower()

        if ext == ".docx":
            return OfficeMetadata._extract_docx(path)

        if ext == ".xlsx":
            return OfficeMetadata._extract_xlsx(path)

        return MetadataInfo(
            file_type="Office",
            summary={},
            full_data={}
        )

    @staticmethod
    def _extract_docx(path):

        doc = Document(path)

        props = doc.core_properties

        summary = {
            "Autor": props.author,
            "Título": props.title,
        }

        full_data = {
            "Autor": props.author,
            "Título": props.title,
            "Assunto": props.subject,
            "Categoria": props.category,
            "Comentários": props.comments,
            "Empresa": props.category,
        }

        return MetadataInfo(
            file_type="DOCX",
            summary=summary,
            full_data=full_data
        )

    @staticmethod
    def _extract_xlsx(path):

        wb = load_workbook(
            path,
            read_only=True
        )

        props = wb.properties

        summary = {
            "Autor": props.creator,
            "Planilhas": len(
                wb.sheetnames
            ),
        }

        full_data = {
            "Autor": props.creator,
            "Último Autor": props.lastModifiedBy,
            "Planilhas": ", ".join(
                wb.sheetnames
            )
        }

        return MetadataInfo(
            file_type="XLSX",
            summary=summary,
            full_data=full_data
        )