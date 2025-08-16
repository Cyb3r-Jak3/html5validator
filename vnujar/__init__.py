import hashlib

updated_at = "2025-08-12"

__all__ = [
    "updated_at",
    "check_sha_hash",
]


def check_sha_hash() -> bool:
    """Check if the SHA hash of vnu.jar matches the expected value."""
    jar_location = __file__.replace('__init__.pyc', 'vnu.jar').replace('__init__.py', 'vnu.jar')
    sha1 = hashlib.sha1()
    with open(jar_location, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            sha1.update(chunk)
            chunk = f.read(4096)
    calculated = sha1.hexdigest()
    with open(jar_location +".sha1", "r") as sha_file:
        sha_hash = sha_file.read().strip()
    if calculated != sha_hash:
        return False
    return True