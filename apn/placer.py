'''
Dataset
https://www.placer.ca.gov/departments/communitydevelopment/gis

Community Development, Geographic Information Systems
530-745-3000
cdrait@placer.ca.gov
'''

import invoke
import rapidjson
from unipath import Path
from .utils import DATA_DIR, build_polygon, convert_geometry, download, unpack, shp_to_geojson, upload


DATASET_URL = 'https://www.dropbox.com/s/ifrbssf88tnzenh/Placer_2016-03-16.zip?dl=1'

local_archive = Path(DATA_DIR, 'CA-Placer.zip')
local_data = Path(DATA_DIR, 'CA-Placer')


def build_documents(data):
    for feature in data['features']:
        apn = feature['properties']['APN']
        if apn is None:
            continue
        document = {
            'apn': apn,
            'state': 'CA',
            'county': 'Placer',
            'year': 2016,
            'boundary': convert_geometry(feature['geometry'])
        }
        yield document


@invoke.task
def placer():
    # Download, if needed
    if not local_archive.exists():
        # raise ValueError('No archive, dummy!')
        download(DATASET_URL, local_archive.name)

    # Unpack the archive
    if not local_data.exists():
        unpack(local_archive)

    geojson_file = Path(local_data, 'Parcels_Poly.geojson')

    if not geojson_file.exists():
        shp_to_geojson(Path(local_data, 'Parcels_Poly.shp'))

    data = rapidjson.loads(open(geojson_file, 'r').read())
    upload(build_documents(data))
