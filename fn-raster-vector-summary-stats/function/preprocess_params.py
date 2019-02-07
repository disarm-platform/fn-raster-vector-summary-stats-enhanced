from preprocess_helpers import download_or_convert_from_base64


def preprocess(params: dict):
    download_or_convert_from_base64('subject', params)
    download_or_convert_from_base64('raster', params)

