import hashlib


def hash_file(path):
    """Return the SHA-1 hash of a file's raw bytes as a hex string."""
    sha1 = hashlib.sha1()

    with open(path, "rb") as file:
        while chunk := file.read(8192):
            sha1.update(chunk)

    return sha1.hexdigest()
