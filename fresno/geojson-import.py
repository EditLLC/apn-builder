import montage
import rapidjson

client = montage.Client('apn-builder', '7b1e530a0a251598bd81960628bd8d3b56fd20c6')
apns = rapidjson.loads(open('fresno-parcels.json', 'r').read())
total = len(apns)
batch = []

for index, (apn, boundary) in enumerate(apns.items()):
    document = {
        'apn': apn,
        'state': 'CA',
        'county': 'Fresno',
        'boundary': boundary
    }
    batch.append(document)

    if len(batch) == 200:
        client.documents.save('apn', *batch)
        batch = []
    print("{index} of {total} - {apn}".format(
        index=index,
        total=total,
        apn=apn,
    ))

if batch:
    client.documents.save('apn', *batch)
