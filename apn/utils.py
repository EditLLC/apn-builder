import os
import zipfile

import geojson
import montage
import requests
from invoke import run
from unipath import Path
from multiprocessing.dummy import Pool

DATA_DIR = Path(Path(__file__).absolute().ancestor(2), 'data')


def build_polygon(coords):
    polygon = geojson.Polygon(coords)
    check = geojson.is_valid(polygon)
    if check['valid'] == 'yes':
        return polygon


def convert_geometry(geometry):
    results = []
    if geometry is None:
        pass
    elif geometry['type'] == 'Polygon':
        polygon = build_polygon(geometry['coordinates'])
        if polygon is not None:
            results.append(polygon)

    elif geometry['type'] == 'MultiPolygon':
        for coords in geometry['coordinates']:
            polygon = build_polygon(coords)
            if polygon is not None:
                results.append(polygon)

    return results


def normalize(apn):
    input_apn = apn
    apn = input_apn.replace('-', '')
    return apn


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
    return jsonfile


def upload(data):
    def worker(doc):
        client = montage.Client('apn-builder', os.environ.get('MONTAGE_TOKEN'))

        query = montage.Query('apn').get_all(doc['apn'], index='apn').filter(
            montage.Field('county') == doc['county'],
            montage.Field('state') == doc['state'],
            montage.Field('year') == doc['year'],
        ).count()

        response = client.execute(query=query)

        message = "[{status}] {doc[county]}, {doc[state]}: {doc[apn]}"
        if response['data']['query'] == 0:
            print(message.format(status='save', doc=doc))
            return doc
        else:
            print(message.format(status='dupe', doc=doc))

    client = montage.Client('apn-builder', os.environ.get('MONTAGE_TOKEN'))

    pool = Pool(processes=10)
    docs = pool.imap(worker, data)

    batch = []
    for doc in (doc for doc in docs if doc is not None):
        batch.append(doc)
        if len(batch) >= 200:
            print('Saving batch...')
            client.documents.save('apn', *batch)
            batch = []
    if batch:
        print('Saving batch...')
        client.documents.save('apn', *batch)
