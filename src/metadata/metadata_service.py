from pathlib import Path

from .generic_metadata import GenericMetadata
from .image_metadata import ImageMetadata
from .pdf_metadata import PdfMetadata
from .office_metadata import OfficeMetadata
from .zip_metadata import ZipMetadata


class MetadataService:

    IMAGE_TYPES = {
        ".jpg",
        ".jpeg",
        ".tif",
        ".tiff",
        ".png",
        ".heic"
    }

    OFFICE_TYPES = {
        ".docx",
        ".xlsx",
    }

    @staticmethod
    def extract(path):

        suffix = Path(
            path
        ).suffix.lower()

        if suffix in MetadataService.IMAGE_TYPES:
            return ImageMetadata.extract(path)

        if suffix == ".pdf":
            return PdfMetadata.extract(path)

        if suffix in MetadataService.OFFICE_TYPES:
            return OfficeMetadata.extract(path)

        if suffix == ".zip":
            return ZipMetadata.extract(path)

        return GenericMetadata.extract(path)