import base64
import hashlib
import json
import os
import uuid
from os import path
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Mutates the params, replacing with local temporary file if required
import config

def required_exists_not_null(key, params):
    pass


def download_or_convert_from_base64(key, params):
    if key not in params:
        raise ValueError(f'Uh oh. {key} not found in params. Probably missing a check in pre-processing step.')

    value = params[key]

    if not isinstance(value, str):
        # Is an object, guessing is JSON
        write_to_file(key, params)
    elif is_url(value):
        download_to_file(key, params)
    else:
        decode_base64_to_file(key, params)


# Extracts the value from params and writes string to a temp file
# Mutates params
def write_to_file(key, params):
    value = params[key]

    hash = hash_this(value)
    filename = get_file_path()

    # Write STRING to file
    open(filename, 'w').write(json.dumps(value))

    params[key] = filename


# Extracts the URL from params, downloads from URL and writes bytes to a temp file
# Mutates params
def download_to_file(key: str, params: dict):
    url = params[key]

    hash = hash_this(url)
    filename = get_file_path(temp=False, force_name=hash)

    if not path.exists(filename):
        # Download from URL to temporary file
        urlretrieve(url, filename)

    # Replace params[key] with temporary file name
    params[key] = filename


# Extracts the value from params, decodes from base64 string and writes to a temp file
# Mutates params
def decode_base64_to_file(key: str, params: dict):
    value = params[key]

    # Decode base64 string
    decoded = base64.b64decode(bytes(value, "utf-8"))

    filename = get_file_path()

    # Write BYTES to file
    open(filename, 'wb').write(decoded)

    # Write to temporary file
    # Replace params[key] with temporary file name
    params[key] = filename


# https://stackoverflow.com/a/52455972/678255
def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Return MD5 hash of URL
def hash_this(string: str) -> str:
    return hashlib.md5(str(string).encode('utf-8')).hexdigest()


# Create a filename for writing
# Creating this using tempfile.NamedTemporaryFile() or similar results in the file
# being closed as soon as the context manager closes: doesn't seem to be another way
# to keep the temporary file around long enough to be used in the runner.
def get_file_path(temp: bool = True, force_name: str = ''):
    file_name = force_name or uuid.uuid4().hex
    if temp:
        return os.path.join(config.TEMP, file_name)
    else:
        return os.path.join('/tmp', file_name)
