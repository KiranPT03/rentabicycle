from flask import Flask, request, url_for, jsonify, redirect
from user_auth import User
from stand import Stand

user = User('NULL', 'NULL', 'NULL')

stand = Stand('NULL', 'NULL', 'NULL')

app = Flask(__name__)


# This API is Not Exposed to Mobile Application
@app.route('/usr-mgmt/register', methods=['POST', 'GET'])
def user_registration():
    """
    Route function for User registration
    :return: Redirects corresponding to user-id
    """
    if request.method == 'POST':
        """ Validating for Content-Type in the request """
        if request.headers['Content-Type'] == 'application/json':
            user_data = request.json  # user_data: payload received during request in form of JSON
            print(user_data)
            """ Parsing payload and passing user register function """
            # TODO : Put JSONSchema validation for received request
            try:
                response = user.register(user_data['properties']['mobile'], user_data['properties'], user_data['geometry'])
                if response['status'] == 'RES_CREATED':
                    return jsonify(response), 201
                elif response['status'] == 'ALREADY_EXISTS':
                    return jsonify(response), 409
                else:
                    return jsonify(response), 400
            except KeyError as key:
                print(key)
                message = 'Validation Error ! Missing Key : ' + str(key)
                response = {'status': 'BAD_REQUEST', 'message': message}
                return jsonify(response), 400
        else:
            response = {'status': 'UNSUPPORTED_MEDIA', 'message': 'Not Supported Content Type'}
            return jsonify(response), 415
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


@app.route('/usr-mgmt/users/<user_id>', methods=['GET'])
def user_info(user_id):
    """
    Function to get user data based on user_id.
    :param user_id: An unique identifier provided during time registration.
    :return: All user information based on user_id selected includes user_info, subscription etc
    """
    if request.method == 'GET':
        try:
            auth_key = request.headers['Authorization']
            response = user.info(user_id, auth_key)
            if response['status'] == 'RES_OK':
                return jsonify(response), 200
            elif response['status'] == 'AUTH_ERR':
                return jsonify(response), 401
            else:
                return jsonify(response), 400
        except KeyError as key:
            print(key)
            message = 'Validation Error ! Missing Key : ' + str(key)
            response = {'status': 'BAD_REQUEST', 'message': message}
            return jsonify(response), 400
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


@app.route('/usr-mgmt/login', methods=['POST'])
def user_login():
    """
    Function responsible for authorizing user during login based on credential provided in payload.
    It generates secure Token using JWT and shares with requested client
    :return: JSON response of login status success/failure
    """
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            user_data = request.json
            print(user_data)
            try:
                response = user.login(user_data['properties']['mobile'], user_data['properties'], user_data['geometry'])
                if response['status'] == 'RES_OK':
                    return jsonify(response), 200
                elif response['status'] == 'NOT_FOUND':
                    return jsonify(response), 404
                else:
                    return jsonify(response), 400
            except KeyError as key:
                message = 'Validation Error ! Missing Key : ' + str(key)
                response = {'status': 'BAD_REQUEST', 'message': message}
                return jsonify(response), 400
        else:
            response = {'status': 'UNSUPPORTED_MEDIA', 'message': 'Not Supported Content Type'}
            return jsonify(response), 415
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


@app.route('/usr-mgmt/logout', methods=['POST'])
def user_logout():
    """
    Function for logging out the session for user based on user_id
    :return: JSON response for Logout call success/failure
    """
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            user_data = request.json
            try:
                auth_key = request.headers['Authorization']
                response = user.logout(auth_key, user_data['properties'])
                if response['status'] == 'RES_OK':
                    return jsonify(response), 200
                elif response['status'] == 'AUTH_ERR':
                    return jsonify(response), 401
                elif response['status'] == 'NOT_FOUND':
                    return jsonify(response), 404
                else:
                    return jsonify(response), 400
            except KeyError as key:
                message = 'Validation Error ! Missing Key : ' + str(key)
                response = {'status': 'BAD_REQUEST', 'message': message}
                return jsonify(response), 400
        else:
            response = {'status': 'UNSUPPORTED_MEDIA', 'message': 'Not Supported Content Type'}
            return jsonify(response), 415
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


# This function is not exposed to Mobile Application
@app.route('/stand-mgmt/register', methods=['POST'])
def stand_registration():
    """
    Function for registering stand in the network includes stand name, manager, contact, no. of bicycles in stand,
    stand coordinates
    :return: JSON response for registration SUCCESS/FAILURE
    """
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            stand_data = request.json  # stand_data: payload received during request in form of JSON
            print(stand_data)
            try:
                response = stand.register(stand_data['properties']['stand_id'], stand_data['properties'],
                                          stand_data['geometry'])
                print(response)
                if response['status'] == 'RES_CREATED':
                    return jsonify(response), 201
                else:
                    return jsonify(response), 400
            except KeyError as key:
                message = 'Validation Error ! Missing Key : ' + str(key)
                response = {'status': 'BAD_REQUEST', 'message': message}
                return jsonify(response), 400
        else:
            response = {'status': 'UNSUPPORTED_MEDIA', 'message': 'Not Supported Content Type'}
            return jsonify(response), 415
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


@app.route('/stand-mgmt/stands/<stand_id>', methods=['GET'])
def stand_info(stand_id):
    if request.method == 'GET':
        print(stand_id)
        response = stand.stand_info(stand_id)
        return jsonify(response), 200


@app.route('/usr-mgmt/users/<user_id>/nearby-stands', methods=['GET'])
def nearby_stand(user_id):
    """
    Function to perform get action on nearby-stands based on users query
    :param user_id: unique identifier assigned for user during login
    :return: JSON response which contains status SUCCESS/FAILURE along with nearby stand data
    """
    if request.method == 'GET':
        try:
            print(user_id)
            auth_key = request.headers['Authorization']
            # From query getting parameters like long, lat, stand_id
            if request.args.get('long') is not None and request.args.get('lat') is not None:
                long = request.args.get('long')
                lat = request.args.get('lat')
                response = user.nearby_stands(user_id, long, lat, auth_key)
                if response['status'] == 'RES_OK':
                    return jsonify(response), 200
                elif response['status'] == 'AUTH_ERR':
                    return jsonify(response), 401
                elif response['status'] == 'NOT_FOUND':
                    return jsonify(response), 404
                else:
                    return jsonify(response), 400
            elif request.args.get('stand_id') is not None:
                response = user.select_stand(user_id, auth_key)
                if response['status'] == 'RES_OK':
                    stand_id = request.args.get('stand_id')
                    url = '/stand-mgmt/stands/'+stand_id
                    return redirect(url)
                elif response['status'] == 'AUTH_ERR':
                    return jsonify(response), 401
                elif response['status'] == 'NOT_FOUND':
                    return jsonify(response), 404
                else:
                    return jsonify(response), 400
            else:
                response = {'status': 'BAD_REQUEST', 'message': 'Unsupported Query!!!'}
                return jsonify(response), 400
        except KeyError as key:
            message = 'Validation Error ! Missing Key : ' + str(key)
            response = {'status': 'BAD_REQUEST', 'message': message}
            return jsonify(response), 400
    else:
        response = {'status': 'METHOD_NOT_ALLOWED', 'message': 'Invalid request method'}
        return jsonify(response), 405


@app.route('/usr-mgmt/users/<user_id>/bicycles/<device_id>/configure', methods=['POST'])
def bicycle_configuration(user_id, device_id):
    pass


@app.route('/usr-mgmt/users/<user_id>/bicycles/<device_id>/end-trip', methods=['POST'])
def bicycle_endtrip(user_id, device_id):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
