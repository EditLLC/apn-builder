'''
Dataset
http://www.co.fresno.ca.us/DepartmentPage.aspx?id=52122

Assessor's Office, Mapping Department
559-600-3585
'''

import invoke
import rapidjson
from unipath import Path
from .utils import DATA_DIR, build_polygon, convert_geometry, download, unpack, shp_to_geojson, upload


DATASET_URL = 'http://www.co.fresno.ca.us/ViewDocument.aspx?id=52154'

local_archive = Path(DATA_DIR, 'CA-Fresno.zip')
local_data = Path(DATA_DIR, 'CA-Fresno')


def build_documents(data):
    for feature in data['features']:
        apn = feature['properties']['APN']
        if apn is None:
            continue
        document = {
            'apn': apn,
            'state': 'CA',
            'county': 'Fresno',
            'year': 2016,
            'boundary': convert_geometry(feature['geometry'])
        }
        yield document


@invoke.task
def fresno():
    # Download, if needed
    if not local_archive.exists():
        download(DATASET_URL, local_archive.name)

    # Unpack the archive
    if not local_data.exists():
        unpack(local_archive)

    geojson_file = Path(local_data, 'Fresno_Parcels.geojson')

    if not geojson_file.exists():
        shp_to_geojson(Path(local_data, 'Fresno_Parcels.shp'))

    data = rapidjson.loads(open(geojson_file, 'r').read())
    upload(build_documents(data))
