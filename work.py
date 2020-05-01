import base64
import json

x = '{"data":"eyJFIjoiRCIsICJUUyI6IjIwMTgxNzEyIn0\\u003d","niddConfiguration":"http://127.0.0.1:27310/SCEF/3gpp-nidd/v1/NIDD_app1/' \
    'configurations/cd9a4a30-5271-4a1e-946a-74e67c5b05a9",' \
    '"msisdn":"915753040000254","externalId":"405857999994364@AGRAHARI.COM"}'

y = json.loads(x)
result = json.loads(base64.b64decode(y["data"]))
print(result["E"])
