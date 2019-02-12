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


def required_exists(key, params):
    if key not in params:
        raise ValueError(f'Required param \'{key}\' not received.')


def required_boolean(key, params):
    if (key in params) and (type(params[key]) != bool):
        raise ValueError('Param `{key}` must be either true or false (JSON boolean)')


def write_temp_from_url_or_base64(key, params):
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

    # get Etag from URL
    # check if not path.exists(filename.etag)
    # else touch filename.etag

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
