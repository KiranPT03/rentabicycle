from database import Database
from shapely.geometry import Polygon, Point, mapping
import json

db = Database('NULL', 'NULL')


class Stand:
    def __init__(self, key, properties, geometry):
        self.key = key
        self.properties = properties
        self.geometry = geometry

    def stand_ref_point(self, lon_point_list, lat_point_list):
        polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
        stand_ref_pt = polygon_geom.representative_point()
        return stand_ref_pt

    def validate_data(self, data, keys):
        for key in keys:
            try:
                if data[key] == "":
                    message = 'Validation Error ! Received NULL value : ' + key
                    return {'status': 'BAD_REQUEST', 'message': message}
            except KeyError as e:
                message = 'Validation Error ! Missing parameter : ' + str(e)
                return {'status': 'BAD_REQUEST', 'message': message}
        return {'status': 'VALID', 'message': 'VALID DATA'}


    def register(self, stand_id, properties, geometry):
        latitude = []
        longitude = []
        #req_property_keys = ['']
        #try:
        #   info = self.validate_data(properties, )
        for x in geometry['coordinates']:
            print(x)
            print(len(x))
            i = 0
            while i < len(x):
                print(x[i])
                latitude.append(x[i][1])
                longitude.append(x[i][0])
                i = i+1
        stand_ref_point = self.stand_ref_point(longitude, latitude)
        stand_ref_point = mapping(stand_ref_point)
        print(stand_ref_point)
        db.set_geo_point('Stand', stand_ref_point['coordinates'][0], stand_ref_point['coordinates'][1], properties['stand_id'])
        polygon_cords_size = len(geometry['coordinates'])
        print(polygon_cords_size)
        geometry = json.dumps(geometry)
        latitude = json.dumps(latitude)
        longitude = json.dumps(longitude)
        stand_ref_point = json.dumps(stand_ref_point['coordinates'])
        #except:
        #    return {'status': 'BAD_REQUEST', 'message': 'Database Error'}

        try:
            if db.is_user_exists(stand_id) is 0:
                stand_data = {
                    'type': 'Stand',
                    'stand_id': properties['stand_id'],
                    'name': properties['name'],
                    'contact': properties['contact'],
                    'manager': properties['manager'],
                    'timestamp': properties['timestamp'],
                    'bicycles': properties['bicycles'],
                    'address': properties['address'],
                    'longitude': longitude,
                    'latitude': latitude,
                    'stand_ref_pt': stand_ref_point,
                    'geometry': geometry
                }
                print(stand_data)
                db.set_entry(stand_id, stand_data)
                print(json.loads(db.get_entry(stand_id, 'geometry')))
                return {'status': 'RES_CREATED', 'message': 'Stand Created Successfully'}
            else:
                return {'status': 'BAD_REQUEST', 'message': 'Stand With Similar Credential already available'}
        except KeyError as key:
            message = 'Validation Error ! Missing Key : ' + str(key)
            response = {'status': 'BAD_REQUEST', 'message': message}
            return response
        except:
            return {'status': 'BAD_REQUEST', 'message': 'Database Error'}

    def stand_info(self, stand_id):
        if db.is_user_exists(stand_id) is 1:
            print(db.get_entry(stand_id, 'name'))
            print(db.get_entry(stand_id, 'contact'))
            print(db.get_entry(stand_id, 'manager'))
            print(db.get_entry(stand_id, 'bicycles'))
            print(db.get_entry(stand_id, 'stand_ref_pt'))
            print(db.get_entry(stand_id, 'geometry'))
            stand_properties = {
                'name': db.get_entry(stand_id, 'name'),
                'manager': db.get_entry(stand_id, 'manager'),
                'contact': db.get_entry(stand_id, 'contact'),
                'stand_ref_pt': db.get_entry(stand_id, 'stand_ref_pt'),
                'address': db.get_entry(stand_id, 'address'),
                'bicycles': db.get_entry(stand_id, 'bicycles')
            }
            stand_geometry = json.loads(db.get_entry(stand_id, 'geometry'))
            stand_info = {
                'type': 'Feature',
                'properties': stand_properties,
                'geometry': stand_geometry
            }

            return {'status': 'RES_OK', 'message': 'Stand Information', 'stand_info': stand_info}
        else:
            print('Currently Stand Doesn"t exist')
