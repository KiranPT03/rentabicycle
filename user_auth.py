from database import Database
import jwt
import json
import uuid

db = Database('NULL', 'NULL')


class User:
    def __init__(self, key, properties, geometry):
        """
        Constructor for User
        :param key:
        :param properties:
        :param geometry:
        """
        self.key = key
        self.properties = properties
        self.geometry = geometry

    def validate_user(self, key, member, password):
        """
        Method to validate user with password.
        This function will query to database based on unique key which will return respective data.
        :param key: Unique key with which data is stored
        :param member: member in data retrived from key
        :param password: password to be validated with existing data in database
        :return: true if matched or flase
        """
        try:
            if db.get_entry(key, member) == password:
                return True
            else:
                return False
        except:
            print('Database Error')
            return "database"

    def validate_auth_token(self, key, member, auth_token):
        """
        Function to authorise token sent for each requests
        THis function matches auth key from database with user sent auth key
        :param key: Unique key with which data is stored
        :param member: memeber in data retrived from key
        :param auth_token: Auth sent by user during request
        :return: True if matches or false
        """
        try:
            if db.get_entry(key, member) == auth_token:
                return True
            else:
                return False
        except:
            print('Database Error')
            return 'database'

    def validate_data(self, data, keys):
        """
        Function to validate data requested in payload.
        This will validate data for mandatory keys in particular method.
        Also it will check for NULL data for mandatory keys
        :param data: Requested data from request payload
        :param keys: list of required keys from particular method
        :return: JSON respose with status of valid or invalid with reason as message
        """
        for key in keys:
            try:
                if data[key] == "":
                    message = 'Validation Error ! Received NULL value : ' + key
                    return {'status': 'BAD_REQUEST', 'message': message}
            except KeyError as e:
                message = 'Validation Error ! Missing parameter : ' + str(e)
                return {'status': 'BAD_REQUEST', 'message': message}
        return {'status': 'VALID', 'message': 'VALID DATA'}

    def register(self, mobile, properties, geometry):
        """
        Method of User class responsible for registering user in Database
        :param mobile: Users Mobile no (treated as unique key for storing user_info)
        :param properties: All data of user including contact details
        :param geometry: Current location of user at time of registration (Currently not Utilised)
        :return: status of creation SUCCESS/FAILURE based on user input
        """
        # req_key : required mandatory parameters should be included in request payload
        req_key = ['mobile', 'name', 'password', 'email', 'dist', 'unit', 'timestamp']

        """ Validating data for Mandatory keys and NULL Values """
        # FIXME : Can be removed once json validation is done on API level for registration route
        info = self.validate_data(properties, req_key)
        if info['status'] == 'VALID':
            if db.is_user_exists(mobile) is 0:
                usr_data = {
                    'type': 'user',
                    'mobile': properties['mobile'],
                    'name': properties['name'],
                    'password': properties['password'],
                    'email': properties['email'],
                    'dist': properties['dist'],
                    'unit': properties['unit'],
                    'timestamp': properties['timestamp']
                }
                print(usr_data)
                try:
                    db.set_entry(mobile, usr_data)
                    return {'status': 'RES_CREATED', 'message': 'User Created Successfully'}
                except:
                    return {'message': 'Database Error', 'status': 'NOT_FOUND'}
            else:
                return {'status': 'ALREADY_EXISTS', 'message': 'User Already Exist'}
        else:
            return info

    def login(self, mobile, properties, geometry):
        """
        Method of User Class deals with usernlogin and Providing Auth key and User_id for future communication
        :param mobile: Users Mobile no (treated as unique key for storing user_info)
        :param properties: All data of user including contact details, password
        :param geometry: Current location of user at time of registration (Currently not Utilised)
        :return: Status of request SUCCESS/FAILURE along with Authorization and user_id
        """
        # req_key : required mandatory parameters should be included in request payload
        req_key = ['mobile', 'password', 'timestamp']
        info = self.validate_data(properties, req_key)
        if info['status'] == 'VALID':
            password = properties['password']
            timestamp = properties['timestamp']
            if db.is_user_exists(mobile) is 1:
                if self.validate_user(mobile, 'password', password) is True:
                    user_id = uuid.uuid4().hex
                    encode_message = {'mobile': mobile, 'password': password, 'timestamp': timestamp}
                    encoded_data = jwt.encode(encode_message, 'secret', algorithm='HS256')
                    user_data = {
                        "auth": encoded_data
                    }
                    try:
                        db.set_entry(mobile, user_data)
                        db.set_entry(user_id, {'mobile': mobile})
                        return {'message': 'Logged In Successfully', 'status': 'RES_OK',
                                'Authorization': encoded_data.decode("utf-8"), 'user_id': user_id}
                    except:
                        return {'message': 'Database Error', 'status': 'NOT_FOUND'}
                else:
                    return {'message': 'Invalid Credentials', 'status': 'BAD_REQUEST'}
            else:
                return {'message': 'User Does not exist! Please Register', 'status': 'NOT_FOUND'}
        else:
            return info

    def info(self, user_id, auth_key):
        """
        Method of User used to get all user information including account_info, subscription, previous rides
        :param user_id: Unique identifier for USer created during login
        :param auth_key: Authorization key for validation
        :return: Status of Request inform of JSON along with user_info
        """
        if db.is_user_exists(user_id) is 1:
            """ Getting mobile number associated with user_id created during login """
            mobile = db.get_entry(user_id, 'mobile')
            if self.validate_auth_token(mobile, 'auth', auth_key) is True:
                # FIXME : Try to use redis hgetall for single call
                try:
                    name = db.get_entry(mobile, 'name')
                    email = db.get_entry(mobile, 'email')
                    dist = db.get_entry(mobile, 'dist')
                    unit = db.get_entry(mobile, 'unit')
                    user_info = {
                        'name': name,
                        'mobile': mobile,
                        'email': email,
                        'dist': dist,
                        'unit': unit
                    }
                    response = {
                        'status': 'RES_OK',
                        'message': 'get all user info',
                        'user_info': user_info
                    }
                    return response
                except:
                    return {'message': 'Database Error', 'status': 'NOT_FOUND'}
            else:
                return {'status': 'AUTH_ERR', 'message': 'Unauthorized User!'}
        else:
            return {'message': 'User Does not exist! Please Register', 'status': 'NOT_FOUND'}

    def logout(self, auth_key, properties):
        """
        User Class method for logging out user by validating Auth key
        :param properties: Info of user includes user_id, timestamp etc
        :param auth_key: Authorization key for validating user
        :return: Status in form of JSON whether SUCCESS/FAILURE
        """
        # req_key : required mandatory parameters should be included in request payload
        req_key = ['user_id']
        info = self.validate_data(properties, req_key)
        if info['status'] == 'VALID':
            user_id = properties['user_id']
            if db.is_user_exists(user_id) is 1:
                """ Getting mobile number associated with user_id created during login """
                mobile = db.get_entry(user_id, 'mobile')
                if self.validate_auth_token(mobile, 'auth', auth_key) is True:
                    user_data = {
                        "auth": "NULL"
                    }
                    db.set_entry(mobile, user_data)
                    print('Delete ENtry: ')
                    print(db.delete_entry(user_id))
                    return {'message': 'Logged Out Successfully', 'status': 'RES_OK'}
                else:
                    return {'status': 'AUTH_ERR', 'message': 'Unauthorized User!!!!'}
            else:
                return {'message': 'User Does not exist! Please Register', 'status': 'NOT_FOUND'}
        else:
            return info


    def nearby_stands(self, user_id, longitude, latitude, auth_key):
        """
        Method to find nearby stands based on users current location
        :param user_id: User's unique identifier
        :param longitude: current location longitude of user
        :param latitude: current location latitude of user
        :param auth_key: Authorization key assigned during login
        :return: Number of stands nearby to user based on his initial distance configuaration
        """
        if db.is_user_exists(user_id) is 1:
            """ Getting mobile number associated with user_id created during login """
            mobile = db.get_entry(user_id, 'mobile')
            if self.validate_auth_token(mobile, 'auth', auth_key) is True:
                dist = db.get_entry(mobile, 'dist')
                unit = db.get_entry(mobile, 'unit')
                nearby_stands = db.get_nearby_locations('Stand', longitude, latitude, dist, unit)
                feature_collection = {'type': 'FeatureCollection'}
                features = []
                for x in nearby_stands:
                    feature = {}
                    properties = {}
                    geometry = {}
                    properties['name'] = db.get_entry(x, 'name')
                    geometry['type'] = 'Point'
                    geometry['coordinates'] = json.loads(db.get_entry(x, 'stand_ref_pt'))
                    properties['bicycles'] = db.get_entry(x, 'bicycles')
                    feature['properties'] = properties
                    feature['geometry'] = geometry
                    feature['type'] = 'Feature'
                    features.append(feature)
                feature_collection['Features'] = features
                print(feature_collection)
                return {'status': 'RES_OK', 'message': 'Stand List', 'nearby_stands': feature_collection}
            else:
                return {'status': 'AUTH_ERR', 'message': 'Unauthorized User!!!!'}
        else:
            return {'message': 'User Does not exist! Please Register', 'status': 'NOT_FOUND'}

    def select_stand(self, user_id, auth_key):
        if db.is_user_exists(user_id) is 1:
            mobile = db.get_entry(user_id, 'mobile')
            if self.validate_auth_token(mobile, 'auth', auth_key) is True:
                return {'status': 'RES_OK', 'message': 'User is Authorized'}
            else:
                return {'status': 'AUTH_ERR', 'message': 'Unauthorized User'}
        else:
            return {'status': 'NOT_FOUND', 'message': 'User Not Found'}
