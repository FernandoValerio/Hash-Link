import zipfile
from datetime import datetime

from .metadata_info import MetadataInfo


class ZipMetadata:

    @staticmethod
    def extract(path):

        with zipfile.ZipFile(path) as zf:

            files = zf.infolist()

            total_original = sum(
                f.file_size
                for f in files
            )

            total_compressed = sum(
                f.compress_size
                for f in files
            )

            folders = sum(
                1
                for f in files
                if f.is_dir()
            )

            regular_files = (
                len(files) - folders
            )

            compression = 0

            if total_original > 0:
                compression = round(
                    (
                        1 -
                        (
                            total_compressed /
                            total_original
                        )
                    ) * 100,
                    2
                )

            summary = {
                "Arquivos": regular_files,
                "Pastas": folders,
                "Original": (
                    f"{round(total_original / 1024 / 1024, 2)} MB"
                ),
                "Compactado": (
                    f"{round(total_compressed / 1024 / 1024, 2)} MB"
                ),
                "Compressão": (
                    f"{compression}%"
                )
            }

            full_data = {}

            for index, file in enumerate(files):

                full_data[
                    f"Item {index + 1}"
                ] = file.filename

                full_data[
                    f"Item {index + 1} - Tamanho"
                ] = file.file_size

                full_data[
                    f"Item {index + 1} - Compactado"
                ] = file.compress_size

                full_data[
                    f"Item {index + 1} - Data"
                ] = datetime(
                    *file.date_time
                ).strftime(
                    "%d/%m/%Y %H:%M:%S"
                )

            return MetadataInfo(
                file_type="ZIP",
                summary=summary,
                full_data=full_data
            )