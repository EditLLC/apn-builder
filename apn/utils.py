import os
import zipfile

import geojson
import montage
import requests
from invoke import run
from unipath import Path

DATA_DIR = Path(Path(__file__).absolute().ancestor(2), 'data')


def build_polygon(coords):
    polygon = geojson.Polygon(coords)
    check = geojson.is_valid(polygon)
    if check['valid'] == 'yes':
        return polygon


def convert_geometry(geometry):
    results = []
    if geometry['type'] == 'Polygon':
        polygon = build_polygon(geometry['coordinates'])
        if polygon is not None:
            results.append(polygon)

    elif feature['geometry']['type'] == 'MultiPolygon':
        for coords in geometry['coordinates']:
            polygon = build_polygon(coords)
            if polygon is not None:
                results.append(polygon)

    return results


def download(url, filename):
    response = requests.get(url, stream=True)
    local_file = Path(DATA_DIR, filename)
    with open(local_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_file


def unpack(filename):
    filename = Path(filename)
    assert zipfile.is_zipfile(filename), 'Invalid archive'
    dirname = filename[:-len(filename.ext)]
    zip = zipfile.ZipFile(filename)
    zip.extractall(dirname)
    zip.close()
    return dirname


def shp_to_geojson(shapefile):
    jsonfile = Path('{0}.geojson'.format(shapefile[:-len(shapefile.ext)]))
    command = 'ogr2ogr -f GeoJSON -t_srs crs:84 {geojson} {shape}'
    run(command.format(geojson=jsonfile, shape=shapefile))
    return geojson_file


def upload(data):
    client = montage.Client('apn-builder', os.environ.get('MONTAGE_TOKEN'))
    batch = []

    for index, document in enumerate(data):
        batch.append(document)

        if len(batch) >= 200:
            client.documents.save('apn', *batch)
            batch = []

        print("{doc[county]}, {doc[state]}: {doc[apn]} ({index})".format(
            index=index,
            doc=document,
        ))

    if batch:
        client.documents.save('apn', *batch)
