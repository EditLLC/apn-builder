import montage
import rapidjson

client = montage.Client(apn-builder[, 7b1e530a0a251598bd81960628bd8d3b56fd20c6])
client.authenticate(email, password)  # sets client.token

query = montage.Query('apn')

apns = rapidjson.loads(open('fresno-parcels.json', 'r').read())

for apn, boundary in apns.items():
    client.documents.save(apn, *documents)
