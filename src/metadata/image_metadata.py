from PIL import Image
from PIL.ExifTags import TAGS

from .metadata_info import MetadataInfo


class ImageMetadata:

    @staticmethod
    def extract(path):

        image = Image.open(path)

        exif = image.getexif()

        data = {}

        for tag_id, value in exif.items():

            tag = TAGS.get(
                tag_id,
                str(tag_id)
            )

            data[tag] = str(value)

        summary = {
            "Fabricante": data.get("Make", "N/D"),
            "Modelo": data.get("Model", "N/D"),
            "Data": data.get("DateTime", "N/D"),
            "GPS": "Sim" if "GPSInfo" in data else "Não"
        }

        summary["Dimensões"] = (
            f"{image.width} x {image.height}"
        )

        return MetadataInfo(
            file_type="Imagem",
            summary=summary,
            full_data=data
        )