## Running locally

`echo "{\"subject\": $(cat points.geojson), \"raster\": \"$(base64 tiny_raster.tif)\"}" | python3 index.py
` or similar is helpful.


Based off DiSARM work: https://github.com/disarm-platform/fn-raster-vector-summary-stats
