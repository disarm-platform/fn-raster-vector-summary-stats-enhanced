# Raster vector summary stats (fn-raster-vector-summary-stats)

Extract summary statistics from raster data for given polygons or points.

## Parameters

JSON object containing:

- `raster`: _{string: Base64-encoded image file or URL}_ Source raster containing values to extract.
- `subject`: _{GeoJSON FeatureCollection of Polygons or Points, URL}_ GeoJSON of polygons or points.
- `stat`: _{array of Strings}_ For _polygons_, pass one or more of `mean`, `max`, `min`, `mode`, `sum`, `count`. Ignored for _points_.
- `geojson_out`: _{boolean}_ Return incoming GeoJSON with additional properties. Default `true`.

## Constraints

- maximum size of `polygons` is ~XX MB or ~YY polygons or ~ZZ total area in kms

## Response

Depending on `geojson_out` above:

- if true, return incoming GeoJSON with calculated statistics added to the `properties` key for each `feature`
- if false, return a JSON array of the calculated statistics

For _points_, the extracted value will be added as a property named `value`.

## Use cases

### WorldPop 1km population extractor

Use `worldpop-1km:latest` as the `raster` parameter.

