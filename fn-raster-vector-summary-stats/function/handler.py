import json

import fiona
from rasterstats import zonal_stats, point_query
from geojson import FeatureCollection


def run_function(params):
    # Prepare the parameters
    subject = params['subject']
    raster = params['raster']
    stats = params.get('stats', 'sum')
    geojson_out = params.get('geojson_out', True)

    try:
        loaded_subject = fiona.open(subject)
        subject_type = loaded_subject.schema['geometry']

        if subject_type == 'Polygon':
            features = zonal_stats(loaded_subject, raster, stats=stats, geojson_out=geojson_out)
        elif subject_type == 'Point':
            features = point_query(loaded_subject, raster, geojson_out=geojson_out)
        else:
            raise ValueError("Input features need to be either all Polygons or Points. Doesn't look like they are.")

        # Decorate return as either GeoJSON FeatureCollection (other way to do this?) or just the array of stats
        if geojson_out:
            return FeatureCollection(features)
        else:
            return features

    except AttributeError:
        raise ValueError("Error calculating zonalstats. Please confirm every input "
                         "geometry is valid, and contains coordinates")
