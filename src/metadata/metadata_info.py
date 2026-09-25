from dataclasses import dataclass


@dataclass
class MetadataInfo:
    file_type: str
    summary: dict
    full_data: dict