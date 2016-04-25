import montage
import rapidjson

client = montage.Client('apn-builder', 'TOKEN')
apns = rapidjson.loads(open('parcels.json', 'r').read())
total = len(apns)
batch = []

for index, (apn, boundary) in enumerate(apns.items()):

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
