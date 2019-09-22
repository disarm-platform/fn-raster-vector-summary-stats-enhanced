# Raster vector summary stats enhanced (fn-raster-vector-summary-stats-enhanced)

Enhanced version of extract summary statistics from raster data for given polygons or points.

Has additional managed caching and speedups.

## Parameters

JSON object containing:

- `raster`: _{string: Base64-encoded image file or URL}_ Source raster containing values to extract.
- `subject`: _{GeoJSON FeatureCollection of Polygons or Points, URL}_ GeoJSON of polygons or points.
- `stats`: _{string}_ Defaults to `mean`. For _polygons_, pass one or more of `mean`, `max`, `min`, `mode`, `sum`, `count` separated by spaces e.g. `max mean`. Not required (and ignored) for _points_.
- `buffer_km`: _{optional, integer}_ If given and the `subject` contains _Points_ (or _MultiPoints_), then the stats will be calculated for a polygon buffering the point by the given distance.
- `geojson_out`: _{boolean}_ Default `true`.
  - For _polygons_: If `true`, return the incoming GeoJSON with additional properties named as given in `stats`. If `false`, return an array of extracted values named as given in `stats`.
  - For _points_: If `true`, return the incoming GeoJSON with an additional property of `value`. If `false`, return an array of the extracted values.

## Constraints

- maximum size of `polygons` is ~XX MB or ~YY polygons or ~ZZ total area in kms

## Response

See `geojson_out` above.

## Example

### Input

```
{
  
}
```

### Output

```
{
}
```


## Use cases

### WorldPop 1km population extractor

Use `worldpop-1km:latest` as the `raster` parameter.

