from preprocess_helpers import write_temp_from_url_or_base64, required_boolean, required_exists


def preprocess(params: dict):
    required_exists('subject', params)
    write_temp_from_url_or_base64('subject', params)

    required_exists('raster', params)
    write_temp_from_url_or_base64('raster', params)

    required_boolean('geojson_out', params)

    # params['stats'] if exists, must only include 'max',
    if 'stats' in params:
        stats = params['stats']
        all_possible_options = ['max', 'min', 'mean']

        for stat in stats.split(' '):
            if stat not in all_possible_options:
                raise ValueError(f'Unsupported `stat` parameter of \'{stat}\'')
