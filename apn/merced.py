'''
Dataset
http://www.co.merced.ca.us/index.aspx?NID=1624

Assessor's Office
209-385-7631
'''

import invoke
import rapidjson
from unipath import Path
from .utils import DATA_DIR, build_polygon, convert_geometry, download, unpack, shp_to_geojson, upload


DATASET_URL = 'https://www.dropbox.com/s/mk7bb9symdume5c/Merced_2016-03-17.zip?dl=1'

local_archive = Path(DATA_DIR, 'CA-Merced.zip')
local_data = Path(DATA_DIR, 'CA-Merced')


def build_documents(data):
    for feature in data['features']:
        apn = feature['properties']['Name']
        if apn is None:
            continue
        document = {
            'apn': apn,
            'state': 'CA',
            'county': 'Merced',
            'year': 2015,
            'boundary': convert_geometry(feature['geometry'])
        }
        if not document['boundary']:
            continue
        yield document


@invoke.task
def merced():
    # Download, if needed
    if not local_archive.exists():
        download(DATASET_URL, local_archive.name)

    # Unpack the archive
    if not local_data.exists():
        unpack(local_archive)

    geojson_file = Path(local_data, 'parcels.geojson')

    if not geojson_file.exists():
        shp_to_geojson(Path(local_data, 'parcels.shp'))

    data = rapidjson.loads(open(geojson_file, 'r').read())
    upload(build_documents(data))
