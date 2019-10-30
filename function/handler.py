import json
import sys

import fiona
from rasterstats import zonal_stats, point_query
from geojson import FeatureCollection
import geopandas as gp
import pandas as pd


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

        is_polygon = 'Polygon' in subject_types or 'MultiPolygon' in subject_types
        is_point = 'Point' in subject_types or 'MultiPoint' in subject_types
        has_buffer = buffer_km is not None

        if is_polygon: # Ignores buffer_km - not buffering polygons
            features = zonal_stats(
                subject, raster, stats=stats, geojson_out=geojson_out)
        elif is_point and not has_buffer:
            features = point_query(
                subject, raster, geojson_out=geojson_out)
        elif is_point and has_buffer:
            buffer_degrees = buffer_km / 111

            original_gdf = gp.GeoDataFrame.from_features(subject)
            subject_gdf = original_gdf.copy()
            subject_gdf.geometry = subject_gdf.buffer(buffer_degrees)
            result = zonal_stats(
                subject_gdf, raster, stats=stats, geojson_out=geojson_out)

            if geojson_out == False:
                # Return directly, skip the 'decoration' below
                features = result
                return features
            else:
                result_gdf = gp.GeoDataFrame.from_features(result)
                result_gdf.geometry = original_gdf.geometry
                features = json.loads(result_gdf.to_json())
                # Return directly, skip the 'decoration' below
                return features 
        else:
            raise ValueError(
                "Input features need to be either all Polygons/MultiPolygons or Points/MultiPoints. Might be a mixture.")

        # Decorate return as either GeoJSON FeatureCollection (other way to do this?) or just the array of stats
        if geojson_out:
            return FeatureCollection(features)
        else:
            return features

    except ValueError as e:
        if e == 'Specify either bounds or window':
            raise ValueError(
                "One or more features are lacking geometry or have null/empty values")

    except AttributeError as e:
        print(e, file=sys.stderr)
        raise ValueError("Error calculating zonal_stats or point_query. Please confirm every input "
                         "geometry is valid, and contains coordinates")


def get_subject_types(subject):
    return set([feature['geometry']['type'] for feature in subject])
