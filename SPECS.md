# Raster vector summary stats enhanced (fn-raster-vector-summary-stats-enhanced)

Enhanced version of extract summary statistics from raster data for given polygons or points.

Has additional managed caching and speedups.

## Parameters

JSON object containing:

- `raster`: _{string: Base64-encoded image file or URL}_ Source raster containing values to extract.
- `subject`: _{GeoJSON FeatureCollection of Polygons or Points, URL}_ GeoJSON of polygons or points.
- `stats`: _{string}_ Defaults to `mean`. Common options are `mean`, `max`, `min`, `mode`, `sum`, `count`. Not required (and ignored) for _points_ without a buffer. For _polygons_, pass a _space_-separated list of one or more: e.g. `sum max`.
- `buffer_km`: _{optional, integer}_ If given and the `subject` contains _Points_ (or _MultiPoints_), then the stats will be calculated for a polygon buffering the point by the given distance. Will be ignored if polygons are provided.
- `geojson_out`: _{boolean}_ Default `true`. 

## Constraints

- maximum size of `subject` is ~XX MB or ~YY polygons or ~ZZ total area in kms

## Response
Depends on `geojson_out`:

- For _polygons_: If `true`, return the incoming GeoJSON with additional properties named as given in `stats`. If `false`, return an array of extracted values named as given in `stats`.
- For _points_ without `buffer_km`: If `true`, return the incoming GeoJSON with an additional property of `value`. If `false`, return an array of the extracted values.
- For _points_ with `buffer_km`: If `false`, return an array of the extracted values. If `true`: return `points` including the stats from the buffered areas. (Plan is to add additional feature to return `buffer_polys`)
