import json
import sys

import fiona
from rasterstats import zonal_stats, point_query
from geojson import FeatureCollection


def run_function(params):
    # Prepare the parameters
    subject_ref = params['subject']
    raster = params['raster']
    stats = params.get('stats', 'mean')
    buffer_km = params.get('buffer_km')
    geojson_out = params.get('geojson_out', True)

    try:
        subject = fiona.open(subject_ref)
        subject_types = get_subject_types(subject)

        if 'Polygon' in subject_types or 'MultiPolygon' in subject_types:
            features = zonal_stats(
                subject, raster, stats=stats, geojson_out=geojson_out)
        elif 'Point' in subject_types or 'MultiPoint' in subject_types:
            if buffer_km is not None:
                buffer_degrees = buffer_km / 111
                polygons = subject.buffer(buffer_degrees)
                features = zonal_stats(
                    polygons, raster, stats=stats, geojson_out=geojson_out)
            else
                features = point_query(subject, raster, geojson_out=geojson_out)
        else:
            raise ValueError(
                "Input features need to be either all Polygons or Points. Doesn't look like they are.")

        # Decorate return as either GeoJSON FeatureCollection (other way to do this?) or just the array of stats
        if geojson_out:
            return FeatureCollection(features)
        else:
            return features
    except ValueError as e:
        if e == 'Specify either bounds or window':
            raise ValueError(
                "One or more features are lacking geometry or have null/empty values")

    except AttributeError:
        raise ValueError("Error calculating zonal_stats or point_query. Please confirm every input "
                         "geometry is valid, and contains coordinates")


def get_subject_types(subject):
    return set([feature['geometry']['type'] for feature in subject])
