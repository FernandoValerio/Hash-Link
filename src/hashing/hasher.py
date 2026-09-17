import hashlib
from pathlib import Path


SUPPORTED_ALGORITHMS = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
    "SHA3-256": "sha3_256",
    "SHA3-512": "sha3_512",
    "BLAKE2b": "blake2b",
}


def calculate_hash(
    file_path: str | Path,
    algorithm: str,
    chunk_size: int = 1024 * 1024,
) -> str:

    algorithm_name = SUPPORTED_ALGORITHMS[algorithm]

    hasher = hashlib.new(algorithm_name)

    with open(file_path, "rb") as file:

        while chunk := file.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()