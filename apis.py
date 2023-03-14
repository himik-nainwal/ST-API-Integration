# Author: Santosh
import base64

import math
import random

import sys

import numpy as np
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
import pymysql as mysql
from flask import make_response
from collections import OrderedDict

sql_connection_string = {'host': 'localhost',
                         'user': 'root',
                         'password': 'root@admin',
                         'database': 'camsec_database'
                         }

app = Flask(__name__)


def get_response(status, body):
    response = make_response(body, status)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route("/", methods=["GET", "POST"])
def home():
    return "Welcome to home page"


def generateOTP():
    """
    :param: Nothing
    :return: This function will return a 6 digit otp
    """
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


# 'http://127.0.0.1:5000/api/forgotpassword', methods=['POST']
# 'http://127.0.0.1:5000/api/allcameras', methods=['GET']
# 'http://127.0.0.1:5000/api/getcamera', methods=['POST']
# 'http://127.0.0.1:5000/api/eventoccur', methods=['POST']
# 'http://127.0.0.1:5000/api/addimage', methods=['POST']
# 'http://127.0.0.1:5000/api/camerasettings', methods=['POST']
# 'http://127.0.0.1:5000/api/areaselection', methods=['POST']
# 'http://127.0.0.1:5000/api/adduser', methods=['POST']
# 'http://127.0.0.1:5000/api/register', methods=['POST']
# 'http://127.0.0.1:5000/api/login', methods=['POST']

class HTTPCODES(object):
    SUCCESS = 200
    INTERNAL = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CREATE_SUCCESS = 201
    NO_CONTENT_SUCCESS = 204


def insert_sql_row(command):
    """
    inserts a record the sql query
    :param command: query to be executed
    :return:
    """
    conn = mysql.connect(**sql_connection_string)
    with conn.cursor() as cursor:
        cursor.execute(command)
        conn.commit()
        cursor.execute("SELECT @@IDENTITY")
        row = cursor.fetchone()[0]
    return row


def sql_execute_command(command):
    """
    executes the sql query
    :param command: query to be executed
    :return:
    """
    try:
        conn = mysql.connect(**sql_connection_string)
        with conn.cursor() as cursor:
            cursor.execute(command)
            conn.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def get_sql_result(command):
    """
    executes the sql select query to get the list of values
    :param command: query to be executed
    :return:
    """
    conn = mysql.connect(**sql_connection_string)
    with conn.cursor() as cursor:
        cursor.execute(command)
        columns = [column[0] for column in cursor.description]
        result = list()
        for row in cursor.fetchall():
            result.append(dict(list(zip(columns, row))))
    return result


def get_distinct_sql_result(command):
    """
    executes the sql select query to get the list of values
    :param command: query to be executed
    :return:
    """
    conn = mysql.connect(**sql_connection_string)
    with conn.cursor() as cursor:
        cursor.execute(command)
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(list(zip(columns, row)))
        else:
            return


@app.route('/login1', methods=['POST'])
def add_login1(request):
    """
    :param: request arguments
    :return: User details with successfully message in case of successfully login
    """

    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        # _name = _json['name']
        _email = _json['email']
        _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _email and _password and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if not cursor.execute("SELECT * FROM adduser WHERE email=%s", (_email,)):
                resp = jsonify("Pls Enter Confirm Email ID")
                return resp
            elif not cursor.execute("SELECT * FROM adduser WHERE password=%s", (_password,)):
                resp = jsonify("Pls Enter Confirm Password")
                return resp
            elif cursor.execute("SELECT * FROM adduser WHERE email=%s AND password=%s", (_email, _password,)):
                rows = cursor.fetchone()
                resp = jsonify("Login is successfully")
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# 1

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    """
       :param: request arguments
       :return: After successful login it will return user details
    """
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        if not email:
            res_body = dict(status=False, message="Please provide email")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        if not password:
            res_body = dict(status=False, message="Password not provided! please provide")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        query = 'SELECT id, userid, email FROM addUser WHERE email="{email}" AND ' \
                'password="{password}"'.format(email=email, password=password)
        result = get_distinct_sql_result(query)
        if not result:
            res_body = dict(status=False, message="Invalid username or password")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        user = {
            "id": result.get('id'),
            "username": result.get('userid'),
            "email": result.get('email'),
        }
        res_body = dict(status=True, message="Login successful", user=user)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)
        res_body = dict(status=False, message="Can't Login")
        return get_response(HTTPCODES.FORBIDDEN, res_body)


# 2
@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        name = request.json.get('name')
        # lname = request.json.get('lname')
        email = request.json.get('email')
        mobileno = request.json.get('mobileno')
        userid = request.json.get('userid')
        # industries = request.json.get('industries')
        company = request.json.get('company')
        password = request.json.get('password')
        query = 'SELECT id, userid, email FROM addUser WHERE userid="{userid}" OR ' \
                'email="{email}"'.format(userid=userid, email=email)
        if get_distinct_sql_result(query):
            res_body = dict(status=False, message="Username or email already exists")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        query = f'INSERT INTO adduser (name, email, mobileno, userid, company, password) ' \
                f'VALUES ("{name}", "{email}",' \
                f' "{mobileno}", "{userid}","{company}", "{password}")'
        executed = sql_execute_command(query)
        if not executed:
            res_body = dict(status=False, message="User not registered ! Internal server Error")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        sql = f'SELECT * FROM adduser WHERE email ="{email}"'
        result = get_distinct_sql_result(sql)
        user = {
            "id": result.get('id'),
            "username": result.get('userid'),
            "email": result.get('email'),
        }
        res_body = dict(status=True, message="User registration successful",
                        user=user)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 3
@app.route('/adduser', methods=['POST'])
@cross_origin()
def add_user():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        name = request.json.get('name')
        email = request.json.get('email'),
        mobile_no = request.json.get('mobile')
        # permission = request.json.get("permission_group")
        query = f'UPDATE adduser SET mobileno = "{mobile_no}", permission = "{permission}" ' \
                f'WHERE userid = "{username}" and email = "{email}"'
        result = sql_execute_command(query)
        if not result:
            res_body = dict(status=False, message="User Not added")
            return get_response(HTTPCODES.BAD_REQUEST, res_body)
        updated_data = {
            "user_name": username,
            "email_address": request.json.get('email'),
            "mobile_number": mobile_no
        }
        res_body = dict(status=True, message=f"User successfully added to the group {permission}",
                        updated_data=updated_data)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 4
@app.route('/areaselection', methods=['POST'])
@cross_origin()
def area_selection():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        name = request.json.get('name')
        query = ''
        result = None
        if not result:
            res_body = dict(status=False, message="Area Selection failed")
            return get_response(HTTPCODES.INTERNAL, res_body)
        res_body = dict(status=True, message="Area successfully selected")
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 5
@app.route('/camerasettings', methods=['POST'])
@cross_origin()
def camera_settings():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        camera_id = request.json.get('camera_id')
        camera_name = request.json.get('camera_name')
        assigned_to = request.json.get('assigned_to')
        rtsp_url = request.json.get('rtsp_url')
        ip_address = request.json.get('ip_address')
        query = f'UPDATE addcamera SET name = "{camera_name}", rtsp = "{rtsp_url}", ' \
                f'ipname = "{ip_address}", permission = "{assigned_to}" WHERE id = "{camera_id}"'
        executed = sql_execute_command(query)
        if not executed:
            res_body = dict(status=False, message="Camera Settings Update Failed")
            return get_response(HTTPCODES.BAD_REQUEST, res_body)
        updated_details = {
            "camera_name": camera_name,
            "assigned_to": assigned_to,
            "rtsp_url": rtsp_url,
            "ip_address": ip_address
        }
        res_body = dict(status=True, message="The camera settings have been updated", updated_detais=updated_details)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 6
@app.route('/eventoccur', methods=['POST'])
@cross_origin()
def event_occur():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        camera_id = request.json.get('camera_id')
        events = request.json.get('events')
        event_list = list()
        for key, value in events.items():
            event_list.append(f'{key} = "{value}"')
        sql_query = 'UPDATE addcamera SET ' + ", ".join(event_list) + f' WHERE id = {camera_id}'
        result = sql_execute_command(sql_query)
        if not result:
            res_body = dict(status=False, message="Event occurrence update failed")
            return get_response(HTTPCODES.BAD_REQUEST, res_body)
        res_body = dict(status=True, message="Event occurrence details updated successfully", updated_details=events)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 7
@app.route('/addimage', methods=['POST'])
@cross_origin()
def add_image():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    try:
        images = request.files
        image = images.get('img')
        image_name = image.filename
        image_upload_path = "E:\Sigminous\Images" # Please enter your file path
        query = f'INSERT INTO Images (name, data) VALUES ("{image_name}", LOAD_FILE("{image_upload_path}"))'
        result = sql_execute_command(query)
        if not result:
            res_body = dict(status=False, message="Image upload failed")
            return get_response(HTTPCODES.BAD_REQUEST, res_body)
        res_body = dict(status=True, message="Image uploaded successfully")
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 8
@app.route('/getcamera', methods=['POST'])
@cross_origin()
def get_camera():
    """
       :param: request arguments
       :return: Returns all camera details
    """
    try:
        cam_id = request.json.get('id')
        sql_query = f'SELECT id, name, rtsp, ipname FROM addcamera WHERE id = {cam_id}'
        result = get_distinct_sql_result(sql_query)
        if not result:
            res_body = dict(status=False, message="No Camera found")
            return get_response(HTTPCODES.NOT_FOUND, res_body)
        res_body = dict(status=True, message="Cameras Details successfully fetched", camera_details=result)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 9
@app.route('/areaselection', methods=['POST'])
@cross_origin()
def area_selection1():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    conn = None
    cursor = None
    try:
        name = request_args.get('name')
        email = request_args.get('email')
        password = request_args.get('password')
        conn = mysql.connect(sql_connection_string)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO {users} VALUES ({name}, {email}, {password})".format(
            users=users_table, name=name, email=email, password=password))
        result = cursor.fetchone()
        if not result:
            res_body = dict(status=False, message="User registration failed",
                            data=response_dict)
            return 401, res_body
        res_body = dict(status=True, message="User successfully registered",
                        data=jsonify(rows))
        return 200, res_body
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# 10
@app.route('/areaselection', methods=['POST'])
@cross_origin()
def area_selection2():
    """
       :param: request arguments
       :return: After successful registration it will return user details
    """
    conn = None
    cursor = None
    try:
        name = request_args.get('name')
        email = request_args.get('email')
        password = request_args.get('password')
        conn = mysql.connect(sql_connection_string)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("INSERT INTO {users} VALUES ({name}, {email}, {password})".format(
            users=users_table, name=name, email=email, password=password))
        result = cursor.fetchone()
        if not result:
            res_body = dict(status=False, message="User registration failed",
                            data=response_dict)
            return 401, res_body
        res_body = dict(status=True, message="User successfully registered",
                        data=jsonify(rows))
        return 200, res_body
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


11


@app.route('/allcameras', methods=['GET'])
@cross_origin()
def all_cameras():
    """
       :param: request arguments
       :return: Returns all camera details
    """
    try:
        sql_query = "SELECT id, name, rtsp, ipname FROM addcamera LIMIT 4"
        results = get_sql_result(sql_query)
        if not results:
            res_body = dict(status=False, message="No Camera found")
            return get_response(HTTPCODES.NOT_FOUND, res_body)
        res_body = dict(status=True, message="All cameras Fetched successfully",
                        cameras=results)
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(e)


# 12
@app.route('/forgotpassword', methods=['POST'])
@cross_origin()
def reset_password():
    """
       :param: request arguments
       :return: After successful message after resetting password
    """
    try:
        username = request.json.get('username')
        email = request.json.get('email')
        new_password = request.json.get('new_password')
        if not email:
            res_body = dict(status=False, message="Please old password")
            return get_response(HTTPCODES.BAD_REQUEST, res_body)
        sql_query = f'UPDATE adduser SET password = "{new_password}" WHERE ' \
                    f'username = "{username}" and email = "{email}"'
        result = sql_execute_command(sql_query)
        if not result:
            res_body = dict(status=False, message="Password Update Failed!")
            return get_response(HTTPCODES.FORBIDDEN, res_body)
        res_body = dict(status=True, message="Password successfully Updated")
        return get_response(HTTPCODES.SUCCESS, res_body)
    except Exception as e:
        print(str(e))


# 13
# 14
# 15
# 16


if __name__ == "__main__":
    app.run()
