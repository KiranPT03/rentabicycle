# This class file is used to represent device, which is a bicycle lock

import json

import redis

redis_client: redis.Redis
redis_client = connect = redis.Redis(host='localhost', port=6379, db=0)

class device:
    device_id = None
    IMEI = None
    IMSI = None
    serial_no = None
    latitude = None
    longitude = None
    signal_strength = None
    battery = None
    app_ver = None
    fw_ver = None
    model = None
    make = None
    MSISDN = None
    state = None
    lastSeen = None

    def __init__(self, device_id):
        self.device_id = device_id
        if redis_client.exists(self.device_id) is 1:
            self.IMEI = redis_client.hget(device_id, 'IMEI').decode("utf-8")
            self.IMSI = redis_client.hget(device_id, 'IMSI').decode("utf-8")
            self.serial_no = redis_client.hget(device_id, 'serial_no').decode("utf-8")
            self.latitude = redis_client.hget(device_id, 'lattitude').decode("utf-8")
            self.longitude = redis_client.hget(device_id, 'longitude').decode("utf-8")
            self.signal_strength = redis_client.hget(device_id, 'signal_strength').decode("utf-8")
            self.battery = redis_client.hget(device_id, 'battery').decode("utf-8")
            self.app_ver = redis_client.hget(device_id, 'app_ver').decode("utf-8")
            self.fw_ver = redis_client.hget(device_id, 'fw_ver').decode("utf-8")
            self.model = redis_client.hget(device_id, 'model').decode("utf-8")
            self.MSISDN = redis_client.hget(device_id, 'MSISDN').decode("utf-8")
            self.state = redis_client.hget(device_id, 'state').decode("utf-8")
            self.lastSeen = redis_client.hget(device_id, 'lastSeen').decode("utf-8")
            print(self.device_id + ' Exist')
        else:
            print(self.device_id + ' does not exists, please call func createDevice')

    def createDevice(self, device_id, properties: json):
        if redis_client.exists(properties['MSISDN']) is 0:
            device_data = {
                'type': 'device',
                'IMEI': properties['IMEI'],
                'IMSI': properties['IMSI'],
                'serial_no': properties['serial_no'],
                'latitude': properties['latitude'],
                'longitude': properties['longitude'],
                'app_ver': properties['app_ver'],
                'fw_ver': properties['fw_ver'],
                'signal_strength': properties['signal_strength'],
                'battery': properties['battery'],
                'make': properties['make'],
                'model': properties['model'],
                'state': properties['state'],
                'psm': properties['psm'],
                'register': 0,
                'lastseen': properties['lastseen']
            }
            print(device_data)
            redis_client.hmset(device_id, device_data)
            return {'status': 'RES_CREATED', 'message': 'Device Created Successfully'}
        else:
            return {'status': 'BAD_REQUEST', 'message': 'Device Already Exist'}

    def updateIMEI(self, IMEI):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'IMEI': IMEI})

    def updateIMSI(self, IMSI):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'IMSI': IMSI})

    def updateSerial_no(self, serial_no):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'serial_no': serial_no})

    def updateLattitude(self, lattiude):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'lattiude': lattiude})

    def updatelongitude(self, longitude):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'longitude': longitude})

    def updateSignal_strenght(self, signal_strenght):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'signal_strenght': signal_strenght})

    def updateBattery(self, battery):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'battery': battery})

    def updateApp_ver(self, app_ver):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'app_ver': app_ver})

    def updateFw_ver(self, fw_ver):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'fw_ver': fw_ver})

    def updateModel(self, model):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'model': model})

    def updateMake(self, make):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'make': make})

    def updateState(self, state):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'state': state})

    def updateLastSeen(self, lastSeen):
        if redis_client.exists(self.device_id) is 1:
            redis_client.hmset(self.device_id, {'lastSeen': lastSeen})

    def get_device_property(self, key, member):
        pass
