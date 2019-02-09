import base64
import hashlib
import json
import os
import uuid
from urllib.parse import urlparse
from urllib.request import urlretrieve

# Mutates the params, replacing with local temporary file if required
import config


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

    filename = get_file_name()

    # Write STRING to file
    open(filename, 'w').write(json.dumps(value))

    params[key] = filename


# Extracts the URL from params, downloads from URL and writes bytes to a temp file
# Mutates params
def download_to_file(key: str, params: dict):
    url = params[key]

    filename = get_file_name()

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

    filename = get_file_name()

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
def hash_url(url: str) -> str:
    return hashlib.md5(url.encode('utf-8')).hexdigest()


# Create a random filename in the temporary directory
# Creating this using tempfile.NamedTemporaryFile() or similar results in the file
# being closed as soon as the context manager closes: doesn't seem to be another way
# to keep the temporary file around long enough to be used in the runner.
def get_file_name(temp: bool = True):
    random_string = uuid.uuid4().hex
    if temp:
        return os.path.join(config.TEMP, random_string)
    else:
        return os.path.join('/tmp', random_string)
