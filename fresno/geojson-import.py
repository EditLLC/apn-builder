import montage
import rapidjson

client = montage.Client('apn-builder', 'API')
apns = rapidjson.loads(open('fresno-parcels.json', 'r').read())
total = len(apns)

for index, (apn, boundary) in enumerate(apns.items()):
    document = {
        'apn': apn,
        'state': 'CA',
        'county': 'Fresno',
        'boundary': boundary
    }
    print("{index} of {total} - {apn}".format(
        index=index,
        total=total,
        apn=apn,
    ))
    client.documents.save('apn', document)
