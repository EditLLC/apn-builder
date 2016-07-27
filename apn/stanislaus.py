'''
Dataset
http://gis.stancounty.com/giscentral/public/downloads.jsp?main=4

Assessor's Office
209-525-6461
'''

import invoke
import rapidjson
from unipath import Path
from .utils import DATA_DIR, build_polygon, normalize, convert_geometry, download, unpack, shp_to_geojson, upload


DATASET_URL = 'http://gis.stancounty.com/shapefiles/parcels.zip'

local_archive = Path(DATA_DIR, 'CA-Stanislaus.zip')
local_data = Path(DATA_DIR, 'CA-Stanislaus')


def build_documents(data):
    for feature in data['features']:
        apn = feature['properties']['APN']
        if apn is None:
            continue
        document = {
            'apn': normalize(apn),
            'state': 'CA',
            'county': 'Stanislaus',
            'year': 2016,
            'boundary': convert_geometry(feature['geometry'])
        }
        yield document


@invoke.task
def stanislaus():
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
