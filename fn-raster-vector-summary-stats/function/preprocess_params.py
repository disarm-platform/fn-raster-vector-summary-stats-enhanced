from preprocess_helpers import required_exists_not_null, download_or_convert_from_base64


def preprocess(params: dict):
    required_exists_not_null('subject', params)
    download_or_convert_from_base64('subject', params)
    
    required_exists_not_null('raster', params)
    download_or_convert_from_base64('raster', params)

    # params['geojson_out'] if exists, must be either True or False
    if (params['geojson_out'] != None):
        

    # params['stats'] if exists, must only include 'max', 
    if (params['stats'] != None):
        all_possible_options = ['max', 'min', 'mean']

        unsupported_param = 'egg'
        raise ValueError(f'Unsupported stat parameter of {unsupported_param}')