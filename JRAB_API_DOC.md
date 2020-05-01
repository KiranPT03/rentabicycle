### Jio Rent A Bicycle API Document
This document will provide Application Server (AS) API's for project Jio Rent A Bicycle (JRAB).
This is a first phase api documentation which will provide API's for below mentioned tasks:
* User Authorization
    1. Register
    2. Login
    3. Logout
* Stand Utility
    1. Register
* User utility
    1. Search nearby stands
    2. Get selected stand information

#### User Authorization
___

This will provide basic user authentication functionalities like registration, login, logout etc.

##### Register

This API is used to register a new User in Ecosystem. A Geo-JSON format is used to define standard request bodies.

**URL** : `/api/v1/usr-mgmt/register`

**Method**: `POST`

**Headers**:

|Header|Value|
|---|---|
|Content-Type|application/json|

 **Request Body**:

    {
        "type": "Feature",
        "properties": {
            "mobile": "82dfghjk",
            "name": "XYZ.XYZ",
            "password": "xyz!xyz",
            "email": "xyz@xyz.com",
            "dist": "0.5",
            "unit": "km",
            "timestamp": "UTC timestamp at time of request"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [-64.73, 32.31]
        }
    }


  ***Parameters***

| Parameters  | Description                                     |Value      |M/O|
|-------------|-------------------------------------------------|-----------|---|
|type         |Indicates a single or collection of objects      ||
|properties   |Property  associated with selected objects       ||
|mobile       |Mobile number of the user                        ||
|name         |Name of the user                                 ||
|password     |Password for the account                         ||
|email        |Email address associated with user               ||
|dist         |Maximum distance user can travel                 ||
|unit         |Unit of the distance selected                    ||
|timestamp    |Standard Unix timestamp when request made        ||
|geometry     |Object of geometry defined as per geoJSON format ||
|type         |member of geometry indicates shape               ||
|coordinates  |A geo-coordinates of the Shape                   ||

**Success Responses**

****Code****: ****201****, RES_CREATED

****Content****:

    {
        'message': 'User Created Successfully'
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |405|MTHOD_NOT_ALLOWED|Requested Method Not Allowed|
 |409|ALREADY_EXISTS|User Already Exists|
 |415|UNSUPPORTED_MEDIA|Unsupported Media Type|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }

##### Login

This API is used to login an existing User in Ecosystem. A Geo-JSON format is used to define standard request bodies.
This API will return Authorization token, along with user_id which can be used subsequent requests till logout.

**URL** : `/api/v1/usr-mgmt/login`

**Method**: `POST`

**Headers**:

|Header|Value|
|---|---|
|Content-Type|application/json|

 **Request Body**:

    {
        "type": "Feature",
        "properties": {
            "mobile": "8275127282",
            "password": "xyz!xyz",
            "timestamp": "1545201903"
            },
        "geometry": {
            "type": "Point",
            "coordinates": [-64.73, 32.31]
         }
    }


  ***Parameters***

| Parameters  | Description                                     |Value      |M/O|
|-------------|-------------------------------------------------|-----------|---|
|type         |Indicates a single or collection of objects      |           |
|properties   |Property  associated with selected objects       |           |
|mobile       |Mobile number of the user                        |           |                                  ||
|password     |Password for the account                         |           |
|timestamp    |Standard Unix timestamp when request made        ||
|geometry     |Object of geometry defined as per geoJSON format ||
|type         |member of geometry indicates shape               ||
|coordinates  |A geo-coordinates of the Shape                   ||

**Success Responses**

****Code****: ****200****, RES_OK

****Content****:

    {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtb2JpbGUiOiI4MmRmZ2hqayIsInBhc3N3b3JkIjoieHl6IXh5eiIsInRpbWVzdGFtcCI6IjE1NDUyMDE5MDMifQ.abtXA_KpujkSz9_fq3vmwcM6_v0QimGu6IIWxRvrtF8",
        "message": "Logged In Successfully",
        "status": "RES_OK",
        "user_id": "9b24d81283ca4c0196c609dfcd2f1d13"
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |404|NOT_FOUND|User Not Found|
 |405|METHOD_NOT_ALLOWED|Requested Method Not Allowed|
 |415|UNSUPPORTED_MEDIA|Unsupported Media Type|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }

##### Logout

This API is used to login an existing User in Ecosystem. A Geo-JSON format is used to define standard request bodies.
This API will return Authorization token, along with user_id which can be used subsequent requests till logout.

**URL** : `/api/v1/usr-mgmt/logout`

**Method**: `POST`

**Headers**: `Authorization Required`

|Header|Value|
|---|---|
|Content-Type|application/json|
|Authorization|eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtb2JpbGUiOiI4MmRmZ2hqayIsInBhc3N3b3JkIjoieHl6IXh5eiIsInRpbWVzdGFtcCI6IjE1NDUyMDE5MDMifQ.abtXA_KpujkSz9_fq3vmwcM6_v0QimGu6IIWxRvrtF8|

 **Request Body**:

    {
        "type": "Feature",
        "properties": {
            "user_id": "c68614abcc1a4e6fae65ae1805a60499",
            "timestamp": "1545211429"
            },
        "geometry": {}
    }

  ***Parameters***

| Parameters  | Description                                     |Value      |M/O|
|-------------|-------------------------------------------------|-----------|---|
|type         |Indicates a single or collection of objects      |           |
|properties   |Property  associated with selected objects       |           |
|user_id      |User Unique Identifier shared during login                        |           |                                  ||
|timestamp    |Standard Unix timestamp when request made        ||
|geometry     |Object of geometry defined as per geoJSON format (NULL) ||


**Success Responses**

****Code****: ****200****, RES_OK

****Content****:

    {
        "message": "Logged Out Successfully"
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |401|UNAUTHORIZED|Unauthorized User|
 |404|NOT_FOUND|User Not Exists|
 |405|METHOD_NOT_ALLOWED|Requested Method Not Allowed|
 |415|UNSUPPORTED_MEDIA|Unsupported Media Type|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }

#### Stand Utility
___

This will provide sample functionalities for creating stand, emergency stand contacts

##### Register

This API will provide stand utility methods which will be used to register, edit etc. stand

**URL** : `/api/v1/stand-mgmt/register`

**Method**: `POST`

**Headers**:

|Header|Value|
|---|---|
|Content-Type|application/json|

 **Request Body**:

    {
        "type": "Feature",
        "properties": {
            "stand_id": "stand-827512fgfd7282",
            "name": "JioStand 3",
            "contact": "123456543234",
            "manager": "xyz",
            "address": "RCP Mumbai"
            "timestamp": "UTC timestamp at time of request",
            "bicycles":0
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [19.126833, 74.013457],
                    [19.136848, 73.013427],
                    [19.126795, 73.014534],
                    [19.129164, 73.013576]
                ]
            ]
        }
    }

  ***Parameters***

| Parameters  | Description                                     |Value      |M/O|
|-------------|-------------------------------------------------|-----------|---|
|type         |Indicates a single or collection of objects      ||
|properties   |Property  associated with selected objects       ||
|stand_id     |Unique Identifier of the stand in Ecosystem                        ||
|name         |Name of the stand                                  ||
|manager|Name of the manager of stand ||
|contact     |Contact information of stand owner or maintainer                         ||
|address      |Address of the stand located|            ||
|timestamp    |Standard Unix timestamp when request made        ||
|bicycles|No. of bicycles in the stand||
|geometry     |Object of geometry defined as per geoJSON format ||
|type         |member of geometry indicates shape               ||
|coordinates  |A geo-coordinates of the Shape                   ||

**Success Responses**

****Code****: ****200****, RES_OK

****Content****:

    {
        "message": "Stand Created Successfully",
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |405|METHOD_NOT_ALLOWED|Requested Method Not Allowed|
 |409|ALREADY_EXISTS|User Already Exists|
 |415|UNSUPPORTED_MEDIA|Unsupported Media Type|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }

#### User Utility
___

This will provide user functionalities for user to access stand and bicycles data in Ecosystem.

##### Nearby-Stands

This API will give nearby stand information based on users current location.
This will return multiple stands present nearby of user based on distance set by user.

**URL**: `/api/v1/usr-mgmt/users/<user_id>/nearby-stands?long=<logitude>&lat=<latitude>`

**Method**: `GET`

**Headers**: `Authorization Required`

|Header|Value|
|---|---|
|Authorization|eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtb2JpbGUiOiI4MmRmZ2hqayIsInBhc3N3b3JkIjoieHl6IXh5eiIsInRpbWVzdGFtcCI6IjE1NDUyMDE5MDMifQ.abtXA_KpujkSz9_fq3vmwcM6_v0QimGu6IIWxRvrtF8|

**Success Responses**

****Code****: ****200****, RES_OK

****Content****:

    {
        "message": "Stand List",
        "nearby_stands": {
            "Features": [
                {
                    "geometry": {
                        "coordinates": [
                            19.1269195,
                            73.013284
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "bicycles": "0",
                        "stand_id": "dfghjkllkhcm"
                    },
                    "type": "Feature"
                },
                {
                    "geometry": {
                        "coordinates": [
                            19.126918071071543,
                            73.0135005
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "bicycles": "0",
                        "stand_id": "dfghjklsdfgjnfm"
                    },
                    "type": "Feature"
                },
                {
                    "geometry": {
                        "coordinates": [
                            19.128815539069542,
                            73.014055
                        ],
                        "type": "Point"
                    },
                    "properties": {
                        "bicycles": "0",
                        "stand_id": "qwertyuujhgfds"
                    },
                    "type": "Feature"
                }
            ],
                "type": "FeatureCollection"
            },
        "status": "RES_OK"
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |401|UNAUTHORIZED|Unauthorized user|
 |404|NOT_FOUND|User Not Exists|
 |405|METHOD_NOT_ALLOWED|Requested Method Not Allowed|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }

##### Selected stand Information

This API will give particular selected stand information including its actual geo-coordinates, no. of bicycles,
stand reference point, stand name, manager, contact etc.

**URL**: `/api/v1/usr-mgmt/users/<user_id>/nearby-stands?stand_id=<selected stand_id>`

**Method**: `GET`

**Headers**: `Authorization Required`

|Header|Value|
|---|---|
|Authorization|eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtb2JpbGUiOiI4MmRmZ2hqayIsInBhc3N3b3JkIjoieHl6IXh5eiIsInRpbWVzdGFtcCI6IjE1NDUyMDE5MDMifQ.abtXA_KpujkSz9_fq3vmwcM6_v0QimGu6IIWxRvrtF8|

**Success Responses**

****Code****: ****200****, RES_OK

****Content****:

    {
        "message": "Stand Information",
        "stand_info": {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [19.126833, 74.013457],
                        [19.136848, 73.013427],
                        [19.126795, 73.014534],
                        [19.129164, 73.013576]
                    ]
                ]
            },
            "properties": {
                "bicycles": "0",
                "name": "JioStand 1",
                "manager": "XYZ",
                "contact": "9511651575",
                "stand_ref_point": [19.128815539069542, 73.014055]
            },
            "type": "Feature"
        },
        "status": "RES_OK"
    }

 **Error Response**

 |Error Code|Description|Message|
 |---|---|---|
 |400|BAD_REQUEST|Invalid Syntax or Data|
 |401|UNAUTHORIZED|Unauthorized user|
 |404|NOT_FOUND|User Not Exists|
 |405|METHOD_NOT_ALLOWED|Requested Method Not Allowed|

 ****Example****

 ****Code****: ****400****, BAD_REQUEST

 ****Content****:

    {
        'message': 'Invlid Syntax or data'
    }
