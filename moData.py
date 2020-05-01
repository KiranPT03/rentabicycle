import base64
import datetime
import json

import redis

import device

# This function will be used for parsing all data originating from south bound side
# mo stands for mobile originated.

redis_client: redis.Redis
redis_client = connect = redis.Redis(host='localhost', port=6379, db=0)

class moData:
    msg_id = None
    data = None
    niddConfig = None
    msisdn = None
    externalId = None
    eventType = None
    timeStamp = None
    battery = None
    signal_strength = None
    value = None
    lat = None
    long = None

    def _init_(self):
        pass

    def moData(self, mo_payload):
        payload = json.loads(mo_payload)

        try:
            self.niddConfig = payload['niddConfiguration']
        except:
            print('error while parsing nidd confg')
            pass

        try:
            self.msisdn = payload['msisdn']
        except:
            print('error while parsing msisdn parameter ')
            pass

        try:
            self.externalId = payload['externalId']
        except:
            print('error while parsing externalId parameter ')
            pass

        try:
            self.data = json.loads(base64.b64decode(payload['data']))
        except:
            print('error while parsing externalId parameter ')
            pass

        try:
            self.msg_id = self.data['T']
        except:
            print('error in parsing message ID')
            pass

        try:
            self.eventType = self.data['E']
        except:
            print('error in parsing event type')
            pass

        try:
            self.battery = self.data['B']
        except:
            print('error in parsing Battery')
            pass

        try:
            self.signal_strength = self.data['S']
        except:
            print('error in parsing signalStrength')
            pass

        try:
            self.value = self.data['V']
        except:
            print('error in parsing value')
            pass

        try:
            self.lat = self.data['LAT']
        except:
            print('error in parsing lattitude')
            pass

        try:
            self.lat = self.data['LONG']
        except:
            print('error in parsing longitude')
            pass

        try:
            if redis_client.exists(self.msg_id) is 0:
                device_modata = {
                    'type': 'moData',
                    'msg_id': self.msg_id,
                    'msisdn': self.msisdn,
                    'battery': self.battery,
                    'signal_strength': self.signal_strength,
                    'value': self.value,
                    'lat': self.lat,
                    'long': self.long,
                    'TimeStamp': datetime.datetime.now()
                }
                print(device_modata)
                redis_client.hmset(self.msg_id, device_modata)
                return {'status': 'CREATED', 'message': 'Device MO Data event Created Successfully'}
            else:
                return {'status': 'ERROR'}
        except:
            print('Error in creating new row in DB')
            pass

        deviceLa = device.device(self.msisdn)
        deviceLa.updateLattitude(self.lat)
        deviceLa.updatelongitude(self.long)
        deviceLa.updateSignal_strenght(self.signal_strength)
        deviceLa.updateBattery(self.battery)
        deviceLa.updateLastSeen(self.msg_id)


# example of NIDD mo data
# x = "{\"data\":\"eyJFIjoiRCIsICJUUyI6IjIwMTgxNzEyIn0\\u003d\",\"niddConfiguration\":\"http://127.0.0.1:27310/SCEF/3gpp-nidd/v1/NIDD_app1/configurations/cd9a4a30-5271-4a1e-946a-74e67c5b05a9\",\"msisdn\":\"915753040000254\",\"externalId\":\"405857999994364@AGRAHARI.COM\"}"
# m = moData()
# m.moData(x)
# print(m.data)
# print(m.niddConfig)
# print(m.msisdn)
# print(m.externalId)
