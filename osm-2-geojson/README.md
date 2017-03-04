# Parsing OSM files to JSON and GeoJSON

This parser is intended to use for obtaining polygon coordinates of countries. It will be probably expanded later to handle natural points too.

## Usage
```
./main.py my-osm-file.osm
```

## Requirements
**Python packages:**
* [`country_bounding_boxes`](https://pypi.python.org/pypi/country-bounding-boxes)
* [`geojson`](https://pypi.python.org/pypi/geojson/)
* [`xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html)

## Output
Parsing to regular JSON files (`output/`) and to [GeoJSON objects](http://geojson.org/geojson-spec.html) (`data/`)

## Source data
Main source of data is preferably "Admin 0 - Countries" shapefiles obtained from [Natural Earth data](http://www.naturalearthdata.com/downloads/50m-cultural-vectors/) and converted using pnorman's [`ogr2osm`](https://github.com/pnorman/ogr2osm) with appropriate translation file to get the tags in OSM standard.

Preferred secondary source which is used in hook is `countries.json` from https://github.com/mledoze/countries. This source contains area, borders and currencies informations.

Other sources are python libraries – such as `country_bounding_boxes` python package...

## TODO
More parametrization, remove hardcoded things except hooks...
