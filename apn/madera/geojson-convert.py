import rapidjson
import geojson

apns = {}

geo = rapidjson.loads(open('Madera_Parcels.geojson').read(), use_decimal=True)


def build_polygon(coords):
    polygon = geojson.Polygon(coords)
    valid = geojson.is_valid(polygon)

    if valid['valid'] == 'yes':
        return polygon


for index, feature in enumerate(geo['features']):
    apn = feature['properties']['Parcel']
    if apn is None:
        continue
    # format APN
    input_apn = apn
    apn = input_apn.replace('-', '')
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

f = open('madera-parcels.json', 'w')
f.write(rapidjson.dumps(apns, use_decimal=True, indent=4))
f.close()
