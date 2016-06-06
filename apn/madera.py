'''
Assessor's Office, Cadastral Drafting Department
559-675-7710
assessor@madera-county.com
'''

import invoke
import rapidjson
from unipath import Path
from .utils import DATA_DIR, build_polygon, convert_geometry, download, unpack, shp_to_geojson, upload


DATASET_URL = 'https://www.dropbox.com/s/euib3xnhw5w03aa/Madera_2016-03-15.zip?dl=1'

local_archive = Path(DATA_DIR, 'CA-Madera.zip')
local_data = Path(DATA_DIR, 'CA-Madera')


def build_documents(data):
    for feature in data['features']:
        apn = feature['properties']['Parcel']
        if apn is None:
            continue
        input_apn = apn
        apn = input_apn.replace('-', '')
        document = {
            'apn': apn,
            'state': 'CA',
            'county': 'Madera',
            'year': 2015,
            'boundary': convert_geometry(feature['geometry'])
        }
        yield document


@invoke.task
def madera():
    # Download, if needed
    if not local_archive.exists():
        download(DATASET_URL, local_archive.name)

    # Unpack the archive
    if not local_data.exists():
        unpack(local_archive)

    geojson_file = Path(local_data, 'MADERA_COUNTY_PARCEL_LAYER.geojson')

    if not geojson_file.exists():
        shp_to_geojson(Path(local_data, 'MADERA_COUNTY_PARCEL_LAYER.shp'))

    data = rapidjson.loads(open(geojson_file, 'r').read())
    upload(build_documents(data))
