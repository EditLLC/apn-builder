import rapidjson
import geojson

apns = {}
batch = []

geo = rapidjson.loads(open('Fresno_Parcels.geojson').read(), use_decimal=True)


def build_polygon(coords):
    polygon = geojson.Polygon(coords)
    valid = geojson.is_valid(polygon)

    if valid['valid'] == 'yes':
        return polygon


for index, feature in enumerate(geo['features']):
    apn = feature['properties']['APN']
    if apn is None:
        continue
    print('apn: ', apn, 'index: ', index)
    apns[apn] = []

    if feature['geometry']['type'] == 'Polygon':
        coords = feature['geometry']['coordinates']
        polygon = build_polygon(coords)
        if polygon is not None:
            apns[apn].append(polygon)
        else:
            print('ERROR', apn)
    elif feature['geometry']['type'] == 'MultiPolygon':
        for coords in feature['geometry']['coordinates']:
            polygon = build_polygon(coords)
            if polygon is not None:
                apns[apn].append(polygon)
            else:
                print('ERROR', apn)

f = open('fresno-parcels.json', 'w')
f.write(rapidjson.dumps(apns, use_decimal=True, indent=4))
f.close()

apns = {}
apns = rapidjson.loads(open('fresno-parcels.json', 'r').read())
for index, (apn, boundary) in enumerate(apns.items()):
    document = {
        'apn': apn,
        'state': 'CA',
        'county': 'Fresno',
        'boundary': boundary
    }
    batch.append(document)

f = open('../parcels.json', 'w')
for item in batch:
    f.write(rapidjson.dumps(item))
f.close()
print('Success')
