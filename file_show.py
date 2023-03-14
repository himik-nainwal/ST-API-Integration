import os
# import cv2
import glob
import json
import numpy as np
import pandas as pd

import matplotlib.path as mplPath
from flask import send_file
from datetime import datetime, date
from flask import Flask
import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, Response
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from detect_ocr_final import run
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiple_Cameras_vision import camera_show
from time import time
import numpy as np
import json

# from multiple_Cameras_vision import camera_show
app = Flask(__name__)
path_base = os.getcwd()
global _path
_path = '5.mp4'



def geo_fence(frame, result, pts):
    # [{'class': 'truck',   'score': 0.38004684,    'coordinates': ((125, 345), (339, 824)) },
    #  {'class': 'car',     'score': 0.13005383,    'coordinates': ((125, 345), (339, 824)) },  ]

    # [ [x1, y1, x2, y2, probability, etc, etc ], [] ]
    # [ [1, 2, 3, 4, 5, 6, 7] , [] ]

    #  [x1,x2,y1,y2]

    # (left, top), (right, bottom) = result['coordinates']
    is_Object_Inside_Polygon = False
    # x_ , y_, z_=frame.shape
    # x_, q = y_, x_
    # print(x_,y_)
    # pts = [(x_-1,0),  ((x_-1)//2,0),  ((x_-1)//2,y_-1),   (x_-1,y_-1)]            #entire image

    # pts = [ ()    ]
    poly_path = mplPath.Path(np.array(pts))
    pts = np.array(pts, np.int32)
    pts = pts.reshape((-1, 1, 2))
    # print(frame.shape)
    # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = cv2.polylines(frame, [pts], True, (255, 0, 0), 3)
    # for object in result:
    (x1, y1), (x2, y2) = (result[0][0], result[0][1]), (result[0][2], result[0][3])  # to confirm
    x = x1 + (x2 - x1) // 2
    y = y1 + (y2 - y1) // 2
    #   print(x,y)

    center_point = (x, y)
    # frame = cv2.circle(frame,(x,y), 25, (255,0,0), -1)
    if poly_path.contains_point(center_point):
        # print('person in polygon')
        is_Object_Inside_Polygon = True
        # font=cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(frame,'person inside geo fence',(500,700),font,4,(255,255,255),2,cv2.LINE_AA)
    return is_Object_Inside_Polygon, frame, x, y


def read_images(cap, camera_id, rstp, location):
    error_camera = False
    s, frame = cap.read()
    return frame, camera_id, error_camera, rstp, location


def get_path():
    conn = None
    cursor = None
    # global bc
    # print('bc =====================================================', bc)
    try:
        camera_list = []
        locatin_list = []
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM addcamera ")
        # cursor.execute("SELECT * FROM userlogin WHERE type='useradmin'")
        # cursor.execute("SELECT * FROM addcamera")
        cursor.execute(
            " SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid) as countryname ,(SELECT C.statename FROM addstate C WHERE C.stateid=R.stateid) as statename ,(SELECT T.citiname FROM addcities T WHERE T.citiid=R.citiid) as citiname ,(SELECT Y.areaname FROM addarea Y WHERE Y.areaid=R.areaid) as areaname FROM addcamera R")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            _path = (rows[i]['ip'])
            _location = (rows[i]['areaname'])
            camera_list.append(_path)
            locatin_list.append(_location)
        return camera_list, locatin_list
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# now = datetime.now()
# current_time = now.strftime("%H:%M:%S %d/%m/%Y")
# bc = ''
@app.route('/upload', methods=['GET', 'POST'])
# @cross_origin()
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route("/<section>")
@cross_origin()
def data(section):
    l = ['*.jpg', '*.png', '*.jpeg', '*.JPG']
    assert section == request.view_args['section']
    path = section
    file_name = path.split('/')[-1].split('.')[0]
    for i in l:
        files = glob.glob(os.path.join(os.getcwd(), i))
        for file in files:
            if file.split('/')[-1].split('.')[0] == file_name:
                return send_file(file, mimetype='image/gif')
    return path


@app.route('/searchbylocation', methods=['POST'])
@cross_origin()
def searchbylocation():
    conn = None
    cursor = None
    try:
        print("l ", request.json),
        _json = request.json
        # _location = _json['location']
        _startdate = _json['startdate']
        _enddate = _json['enddate']
        # _numberplate=_json['numberplate']
        if _startdate and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT *  FROM ocr_info WHERE date BETWEEN CAST (date=%s AS DATE) AND CAST (date=%s AS DATE)",
                (_startdate, _enddate))
            # Select * From employee where e_salary BETWEEN 60000 AND 1200000;
            rows = cursor.fetchall()
            resp = jsonify(rows)
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addmaster', methods=['POST'])
@cross_origin()
def add_vehiclemasteraster():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _vehiclename = _json['vehiclename']
        _vehicleclassification = _json['vehicleclassification']
        _status = _json['status']
        if _vehiclename and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM vehiclemaster WHERE vehiclename=%s", (_vehiclename,)):
                resp = jsonify("not enter duplicate Vehicle Name")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO vehiclemaster(vehiclename, vehicleclassification, status) VALUES(%s,%s, %s)"
                data = (_vehiclename, _vehicleclassification, _status,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New Vehicle Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatevehiclemaster', methods=['POST'])
@cross_origin()
def update_updatevehiclemaster():
    conn = None
    cursor = None
    try:
        _json = request.json
        _vid = _json['vid']
        _vehiclename = _json['vehiclename']
        _vehicleclassification = _json['vehicleclassification']
        _status = _json['status']
        if _vehiclename and request.method == 'POST':
            sql = "UPDATE vehiclemaster SET vehiclename=%s,vehicleclassification=%s,status=%s WHERE vid=%s"
            data = (_vehiclename, _vehicleclassification, _status, _vid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatefaremaster', methods=['POST'])
@cross_origin()
def add_updatefaremaster():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _areaid = _json['areaid']
        _fare = _json['fare']
        _status = _json['status']
        _vid = _json['vid']
        _fid = _json['fid']
        # validate the received values
        if _countryid and _fare and request.method == 'POST':
            sql = "UPDATE faremaster SET countryid=%s, stateid=%s, citiid=%s, areaid=%s, fare=%s, status=%s, vid=%s WHERE fid=%s"
            data = (_countryid, _stateid, _citiid, _areaid, _fare, _status, _vid, _fid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            resp = jsonify("Record Updated Successfully")
            return resp
            # if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #   account = cursor.fetchone()
            #   resp=jsonify("user Added Successfully")
            #   return resp

            # # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            # # resp = cursor.fetchone()
            # return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletevehiclemaster', methods=['POST'])
@cross_origin()
def update_deletevehiclemaster():
    conn = None
    cursor = None
    try:
        _json = request.json
        _vid = _json['vid']
        if _vid and request.method == 'POST':
            sql = "DELETE FROM vehiclemaster WHERE vid=%s"
            data = (_vid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addcountry', methods=['POST'])
@cross_origin()
def add_country():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _countryname = _json['countryname']
        if _countryname and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addcountry WHERE countryname=%s", (_countryname,)):
                resp = jsonify("not enter duplicate Country Name")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addcountry(countryname) VALUES(%s)"
                data = (_countryname,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New New Country Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addarea', methods=['POST'])
@cross_origin()
def add_area():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _area = _json['area']
        _countryid = _json['countryid']
        if _area and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addarea WHERE areaname=%s", (_area,)):
                resp = jsonify("not enter duplicate Area Name")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addarea(areaname, stateid, countryid, citiid) VALUES(%s,%s,%s, %s)"
                data = (_area, _stateid, _countryid, _citiid,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New Area Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addcity', methods=['POST'])
@cross_origin()
def add_city():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _stateid = _json['stateid']
        _citiname = _json['citiname']
        _countryid = _json['countryid']
        if _citiname and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addcities WHERE citiname=%s", (_citiname,)):
                resp = jsonify("not enter duplicate City Name")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addcities(stateid, citiname, countryid) VALUES(%s,%s, %s)"
                data = (_stateid, _citiname, _countryid,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New New Country Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addstate', methods=['POST'])
@cross_origin()
def add_state():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _statename = _json['statename']
        _countryid = _json['countryid']
        if _statename and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addstate WHERE statename=%s", (_statename,)):
                resp = jsonify("not enter duplicate State Name")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addstate(statename,countryid) VALUES(%s, %s)"
                data = (_statename, _countryid,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New New Country Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addcamera', methods=['POST'])
@cross_origin()
def add_user():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _laneno = _json['laneno']
        _ip = _json['ip']
        _object_detection = _json['object_detection']
        _crrn_ocr = _json['crnn_ocr']
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _areaid = _json['areaid']
        if _ip and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addcamera WHERE ip=%s", (_ip,)):
                resp = jsonify("not enter duplicate Ip")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addcamera(lane_no, ip, object_detection, crnn_ocr,countryid,stateid,citiid,areaid) VALUES(%s, %s, %s,%s, %s, %s, %s,%s)"
                data = (_laneno, _ip, _object_detection, _crrn_ocr, _countryid, _stateid, _citiid, _areaid,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New Camera Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addgiofence', methods=['POST'])
@cross_origin()
def add_getgiofence():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _width = _json['width']
        _heigt = _json['height']
        _top = _json['top']
        _left = _json['left']
        _cameraid = _json['cameraid']
        if _cameraid and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addgiofence WHERE cameraid=%s", (_cameraid,)):
                resp = jsonify("not enter duplicate top and left Link ")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addcamera(cameraid) VALUES (%s)"
                data = (_cameraid,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('NewGiofence Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updateuser', methods=['POST'])
@cross_origin()
def update_userupdateuser():
    conn = None
    cursor = None
    try:
        _json = request.json
        print(request.json)
        _password = _json['password']
        _email = _json['email']
        _id = _json['id']
        _activeemail = _json['activeemail']
        _aadharimage = _json['aadharimage']
        _type = _json['type']
        _aadharnumber = _json['aadharnumber']
        _status = _json['status']
        _mobileno = _json['mobileno']
        # # validate the received values
        # if _email and _password and request.method == 'POST':
        #     conn = mysql.connect()
        #     cursor = conn.cursor(pymysql.cursors.DictCursor)
        #     if cursor.execute("SELECT * FROM adduser WHERE email=%s AND password=%s",(_email, _password,)):
        #         resp = jsonify("Pls do not enter duplicate Email Id And Password")
        #         return resp
        #     elif cursor.execute("SELECT * FROM adduser WHERE aadhar_number=%s",(_aadharnumber,)):
        #         resp = jsonify("Pls do not enter duplicate Aadhar Number")
        #         return resp 
        #     else:
        #         sql = "INSERT INTO adduser(aadhar_number, aadhar_image, password, mobileno, email, status, activeemail, type) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)"
        #         data = (_aadharnumber, _aadharimage, _password,_mobileno,_email,_status,_activeemail,_type,)
        #         conn = mysql.connect()
        # _json = request.json
        # _cd = _json['countryid']
        # _stateid=_json['stateid']
        # _citiid=_json['citiid']
        # _areaname = _json['areaname']
        # _areaid=_json['areaid']
        if _id and request.method == 'POST':
            sql = "UPDATE adduser SET aadhar_number=%s,aadhar_image=%s,password=%s,mobileno=%s,email=%s,status=%s,activeemail=%s,type=%s WHERE id=%s"
            data = (_aadharnumber, _aadharimage, _password, _mobileno, _email, _status, _activeemail, _type, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addfaremaster', methods=['POST'])
@cross_origin()
def add_datafaremaster():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _areaid = _json['areaid']
        _fare = _json['fare']
        _status = _json['status']
        _vid = _json['vid']
        # validate the received values
        if _countryid and _fare and request.method == 'POST':
            sql = "INSERT INTO faremaster(countryid, stateid, citiid, areaid, fare, status, vid) VALUES(%s, %s, %s, %s,%s,%s,%s)"
            data = (_countryid, _stateid, _citiid, _areaid, _fare, _status, _vid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            resp = jsonify("FareMaster Added Successfully")
            return resp
            # if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #   account = cursor.fetchone()
            #   resp=jsonify("user Added Successfully")
            #   return resp

            # # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            # # resp = cursor.fetchone()
            # return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
@cross_origin()
def add_login1():
    conn = None
    cursor = None
    # msg = ""
    # session=None

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


@app.route('/deleteocr', methods=['POST'])
@cross_origin()
def update_deleteedocrocr():
    conn = None
    cursor = None
    try:
        _json = request.json
        _camD = _json['id']
        if _camD and request.method == 'POST':
            sql = "DELETE FROM ocr_info WHERE id=%s"
            data = (_camD,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('OCR Data Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletefaremaster', methods=['POST'])
@cross_origin()
def update_deletefaremaster():
    conn = None
    cursor = None
    try:
        _json = request.json
        _camD = _json['fid']
        if _camD and request.method == 'POST':
            sql = "DELETE FROM faremaster WHERE fid=%s"
            data = (_camD,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Camera Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getfaremasterlist')
@cross_origin()
def users_getcountrycityerrrcountrygetmaster():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            " SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid) as countryname ,(SELECT C.statename FROM addstate C WHERE C.stateid=R.stateid) as statename ,(SELECT T.citiname FROM addcities T WHERE T.citiid=R.citiid) as citiname ,(SELECT Y.areaname FROM addarea Y WHERE Y.areaid=R.areaid) as areaname,(SELECT V.vehiclename FROM vehiclemaster V WHERE V.vid=R.vid) as vehiclename FROM faremaster R")
        # cursor.execute("SELECT * FROM addarea")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatearea', methods=['POST'])
@cross_origin()
def update_userupdatesttecityareaareaw():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _areaname = _json['areaname']
        _areaid = _json['areaid']
        if _countryid and request.method == 'POST':
            sql = "UPDATE addarea SET areaname=%s,stateid=%s,countryid=%s,citiid=%s WHERE areaid=%s"
            data = (_areaname, _stateid, _countryid, _citiid, _areaid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatecity', methods=['POST'])
@cross_origin()
def update_userupdatesttecity():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _citiname = _json['citiname']
        _citiid = _json['citiid']
        if _countryid and request.method == 'POST':
            sql = "UPDATE addcities SET stateid=%s,citiname=%s,countryid=%s WHERE citiid=%s"
            data = (_stateid, _citiname, _countryid, _citiid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatestate', methods=['POST'])
@cross_origin()
def update_userupdatestte():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        _stateid = _json['stateid']
        _statename = _json['statename']
        if _countryid and request.method == 'POST':
            sql = "UPDATE addstate SET statename=%s,countryid=%s WHERE stateid=%s"
            data = (_statename, _countryid, _stateid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatecountry', methods=['POST'])
@cross_origin()
def update_usercountry():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        _countryname = _json['countryname']
        if _countryid and request.method == 'POST':
            sql = "UPDATE addcountry SET countryname=%s WHERE countryid=%s"
            data = (_countryname, _countryid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update', methods=['POST'])
@cross_origin()
def update_user():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        _camD = _json['camD']
        _ip = _json['ip']
        _location = _json['location']
        _laneno = _json['laneno']
        # validate the received values
        if _camD and request.method == 'POST':
            sql = "UPDATE addcamera SET lane_no=%s, location=%s, ip=%s WHERE camD=%s"
            data = (_laneno, _location, _ip, _camD,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
@cross_origin()
def add_login():
    conn = None
    cursor = None
    # msg = ""
    # session=None

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
            if cursor.execute("SELECT * FROM adduser WHERE email=%s AND password=%s", (_email, _password,)):
                rows = cursor.fetchone()
                resp = jsonify(rows)
                resp.status_code = 200
                return resp
            else:
                resp = jsonify('Pls Enter Valid Emailid And Password!')
                # resp.status_code = 500
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# @app.route('/showuseralert', methods=['POST'])
# @cross_origin()
# def add_login():
#   conn = None
#   cursor = None
#   # msg = ""
#   # session=None

#   try:
#       print("request ",request.json),
#       _json = request.json
#       print("request ",_json)
#       # _name = _json['name']
#       _cameraid = _json['cameraid']
#       # _password = _json['password']
#       # _type= _json['type']
#       # validate the received values
#       if _cameraid and request.method == 'POST':
#           conn = mysql.connect()
#           cursor = conn.cursor(pymysql.cursors.DictCursor)
#           if cursor.execute("SELECT * FROM addimage WHERE cameraid=%s",(_cameraid,)):
#               rows = cursor.fetchall()
#               resp = jsonify(rows)
#               resp.status_code = 200
#               return resp     
#           else:
#               resp = jsonify('Pls Enter Valid cameraid!')
#               # resp.status_code = 500
#               return resp
#       else:
#           return not_found()
#   except Exception as e:
#       print(e)
#   finally:
#       cursor.close() 
#       conn.close()


@app.route('/adduser', methods=['POST'])
@cross_origin()
def add_data():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _password = _json['password']
        _email = _json['email']
        _activeemail = _json['activeemail']
        _aadharimage = _json['aadharimage']
        _type = _json['type']
        _aadharnumber = _json['aadharnumber']
        _status = _json['status']
        _mobileno = _json['mobileno']
        # validate the received values
        if _email and _password and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM adduser WHERE email=%s AND password=%s", (_email, _password,)):
                resp = jsonify("Pls do not enter duplicate Email Id And Password")
                return resp
            elif cursor.execute("SELECT * FROM adduser WHERE aadhar_number=%s", (_aadharnumber,)):
                resp = jsonify("Pls do not enter duplicate Aadhar Number")
                return resp
            else:
                sql = "INSERT INTO adduser(aadhar_number, aadhar_image, password, mobileno, email, status, activeemail, type) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)"
                data = (_aadharnumber, _aadharimage, _password, _mobileno, _email, _status, _activeemail, _type,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                resp = jsonify("user Added Successfully")
                return resp
                # if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
                #   account = cursor.fetchone()
                #   resp=jsonify("user Added Successfully")
                #   return resp

                # # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
                # # resp = cursor.fetchone()
                # return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodelimagesbyid', methods=['POST'])
@cross_origin()
def add_iddouble():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _id = _json['id']
        _industries = _json['industries']
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM model WHERE id=%s AND industries=%s", (_id, _industries,)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchone()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodelintroduction', methods=['POST'])
@cross_origin()
def add_modelintroduction():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT introduction FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchone()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodeldos', methods=['POST'])
@cross_origin()
def add_modelprocessdos():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT do FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodeldont', methods=['POST'])
@cross_origin()
def add_modelprocessdont():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT dont FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def estimateSpeed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    # ppm = location2[2] / carWidht
    ppm = 8.8
    d_meters = d_pixels / ppm
    # print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
    fps = 30
    speed = d_meters * fps * 3.6
    return speed


d = {}


def ocr(_path, _location):
    d1 = {'flag': '', 'labels': ' '}
    l = []
    speed_list = []
    new_speed_list = []
    direction_list = []
    file_name_list = []
    id_list = []
    current_time_list = []
    current_date_list = []
    alert_list = []
    image_name_prev = 'hi'
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # current_date = date.today()
    # current_date_ = current_date.strftime("%x")
    # d = {'Speed': speed_list, 'Direction': direction_list, 'Time': [current_time], 'Date': [current_date_], 'Vehicle': ['Car'], 'Image': []}
    count = 0
    rectangleColor = (0, 255, 0)
    frameCounter = 0
    currentCarID = 0
    fps = 0
    # speed[i] = 0
    carCascade = cv2.CascadeClassifier('myhaar.xml')
    # print('_path-------------------------------------',_path)
    # video = cv2.VideoCapture(_path[0])
    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000
    rlabel = ''
    # Write output to video file
    # out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))

    # print('checking==============================', _path)
    Final_Frame = np.zeros([100, 100, 3], dtype=np.uint8)
    l1 = []
    # print(_path)
    _p = zip(_path, _location)
    for i, (path, area) in enumerate(_p):
        l1.append({"id": i, "rstp": path, "location": area, "show": 1})
    dict2 = {"1": l1}
    # print(dict2)   

    prev_len = 301
    error_in_cameras = [False, False]

    while True:

        camera_data = dict2["1"]

        if len(camera_data) != prev_len:
            camera_list = []
            print(camera_list)
            print(len(camera_data))
            for i in range(len(camera_data)):
                print(camera_data[i]['rstp'])
                # cap=VideoStream(src=camera_data[i]['rstp']).start()
                camera_list.append(
                    [cv2.VideoCapture(camera_data[i]['rstp']), camera_data[i]['id'], camera_data[i]['rstp'],
                     camera_data[i]['location']])

        if any(error_in_cameras):
            for i in range(len(error_in_cameras)):
                # cap=VideoStream(src=camera_data[i]['rstp']).start()
                cap = camera_list[i][0]
                print(f'error ------------------------------------------------- {error_in_cameras}')
                if error_in_cameras[i]:
                    try:
                        print('release')
                        cap.release()

                    except:
                        print('stop')
                        cap.stop()
                    camera_list[i][0] = cv2.VideoCapture(camera_data[i]['rstp'])

        prev_len = len(camera_data)
        show_cameras = []

        for i in range(len(camera_data)):
            if camera_data[i]['show'] == 1:
                show_cameras.append(camera_data[i]['id'])

        processes = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for camera, camera_id, rstp, camera_location in camera_list:
                processes.append(executor.submit(read_images, camera, camera_id, rstp, camera_location))

        frames = []
        labels12 = []
        error_in_cameras = []
        for task in as_completed(processes):
            if task.result()[0] is None:
                frame = np.zeros((680, 480, 3), np.uint8)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Camera number' + str(task.result()[1]) + 'OFF', (200, 300), font, 0.5, (255, 0, 0),
                            2, cv2.LINE_AA)
                error_in_cameras.append(True)
            else:
                _, frame, _, _, _ = run(task.result()[0])
                error_in_cameras.append(False)
            frames.append([frame, task.result()[1]])
            # error_in_cameras.append(task.result()[2])

        frames = sorted(frames, key=lambda x: x[1])
        for f, l in zip(frames, labels12):
            frame_fire = f[0].copy()
            real_label = l
            location_name = f[2]
            image = frame_fire.copy()
            # frames.append(image_frame)
            # cv2.putText(img = frame_fire, text = fire_flag, org = (100, 150), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 1.0, color = (0, 0, 255), thickness = 2)

            # cv2.putText(img = im0, text = f, org = (10, 10), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 3.0, color = (125, 246, 55), thickness = 3)
            Final_Frame = camera_show(id_list=show_cameras, frames_list=frames)
            try:
                LPN = prediction[0]
            except:
                continue

            frameCounter += 1

            carIDtoDelete = []

            for carID in carTracker.keys():
                trackingQuality = carTracker[carID].update(image)

                if trackingQuality < 7:
                    carIDtoDelete.append(carID)

            for carID in carIDtoDelete:
                print('Removing carID ' + str(carID) + ' from list of trackers.')
                print('Removing carID ' + str(carID) + ' previous location.')
                print('Removing carID ' + str(carID) + ' current location.')
                carTracker.pop(carID, None)
                carLocation1.pop(carID, None)
                carLocation2.pop(carID, None)

            if not (frameCounter % 10):

                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

                for (_x, _y, _w, _h) in cars:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    x_bar = x + 0.5 * w
                    y_bar = y + 0.5 * h

                    matchCarID = None

                    for carID in carTracker.keys():
                        trackedPosition = carTracker[carID].get_position()

                        t_x = int(trackedPosition.left())
                        t_y = int(trackedPosition.top())
                        t_w = int(trackedPosition.width())
                        t_h = int(trackedPosition.height())

                        t_x_bar = t_x + 0.5 * t_w
                        t_y_bar = t_y + 0.5 * t_h

                        if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (
                                x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                            matchCarID = carID

                    if matchCarID is None:
                        print('Creating new tracker ' + str(currentCarID))

                        tracker = dlib.correlation_tracker()
                        tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                        carTracker[currentCarID] = tracker
                        carLocation1[currentCarID] = [x, y, w, h]

                        currentCarID = currentCarID + 1

            # #cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)
            # for carID in carTracker.keys():
            #   file_name_list.append(str(carID)+'.png')

            for carID in carTracker.keys():
                trackedPosition = carTracker[carID].get_position()

                t_x = int(trackedPosition.left())
                t_y = int(trackedPosition.top())
                t_w = int(trackedPosition.width())
                t_h = int(trackedPosition.height())

                # cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)

                # speed estimation
                carLocation2[carID] = [t_x, t_y, t_w, t_h]

            # end_time = time.time()

            # if not (end_time == start_time):
            #     fps = 1.0/(end_time - start_time)

            # cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            for i in carLocation1.keys():
                # print('car idssssssssssssssssss',i)

                if frameCounter % 1 == 0:
                    [x1, y1, w1, h1] = carLocation1[i]
                    [x2, y2, w2, h2] = carLocation2[i]

                    img_new = resultImage.copy()
                    img_new = img_new[y1: y1 + h1, x1:x1 + w1]

                    if file_name_list_copy != file_name_list:
                        cv2.imwrite(os.path.join(save_path, str(i) + '.png'), img_new)

                    # print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
                    carLocation1[i] = [x2, y2, w2, h2]

                    # print 'new previous location: ' + str(carLocation1[i])
                    if [x1, y1, w1, h1] != [x2, y2, w2, h2]:

                        if True:
                            sp = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
                            new_speed = (int(sp))
                            speed_new = random.randint(75, 85)
                            new_speed_list.append(speed_new)
                            speed_list.append(new_speed)
                            file_name_list.append(str(i) + '.png')
                            _image = f'{str(i)}.png'
                            direction_list.append(out)
                            current_time_list.append(current_time)
                            current_date_list.append(current_date_)
                            _location = 'Indore'
                            print('location ------------------------------------------------------------', _location)
                            conn = mysql.connect()
                            cursor = conn.cursor(pymysql.cursors.DictCursor)
                            if cursor.execute("SELECT * FROM vids WHERE location=%s", (_location,)):
                                resp = jsonify("Duplicate Value Entered")
                                return resp
                                # print("not enter duplicate data")         
                            else:
                                sql = "INSERT INTO vids(speed, alert_type, date, vehicle, location, image) VALUES(%s,%s, %s, %s, %s, %s)"
                                data = (sp, out, _location, current_date_, rlabel, _image)
                                conn = mysql.connect()
                                cursor = conn.cursor()
                                cursor.execute(sql, data)
                                conn.commit()
                                resp = jsonify('New Data Added Successfully!')
                                resp.status_code = 200
                                return resp
                            # d['Speed'] = new_speed
                            # d['Direction'] = out
                            # d['Image'] = str(i)+'.png'
                            # print('dsssssdsdsdsdsd',i)

                            # if len(l)==0:
                            #   l.append(d)
                            # else:
                            #   if l[-1]['Image']!=d['Image']:
                            #       l.append(d)

                            ocr.var = speed[i]

                    # if speed[i] != None and y1 >= 180:
                    # cv2.putText(resultImage, str(int(speed[i])) + " km/hr", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

                try:
                    for J in range(len(file_name_list)):
                        d = {}

                        d['Speed'] = speed_list[J]
                        # d['Direction'] = direction_list[J]
                        d['Alert'] = alert_list[J]
                        d['Image'] = file_name_list[J]
                        d['Time'] = current_time_list[J]
                        d['Date'] = current_date_list[J]
                        d['Vehicle'] = labels[J]
                        l.append(d)

                except:
                    continue
                    with open('file_name_list.pickle', 'wb') as f:
                        pickle.dump(file_name_list, f)

                    file_name_list_copy = file_name_list

                l_new = []
                numbers_id = []
                speed_list_id = {}
                for i in range(len(l)):
                    if l[i]['image'] not in numbers_id:
                        l_new.append(l[i])
                        # s = pd.Series(data = l_new)
                        df = pd.DataFrame(data=l_new)
                        df.to_csv('test_1.csv')

                    numbers_id.append(l[i]['image'])
                    speed_list_id[l[i]['image']] = l[i]['alert']

                for i in range(len(l_new)):
                    l_new[i]['alert'] = random.randint(81, 100)

                ocr.var2 = out
                df = pd.DataFrame(data=l_new)
                df.to_csv('new_testing_file.csv')
                ocr.var3 = df

                # now = datetime.now()
                # current_time = now.strftime("%H:%M:%S %d/%m/%Y")
                # time = current_time.split(' ')[0]
                # date = current_time.split(' ')[-1]
                # # # print('----------------------------------- prediction  -----------------------------------', prediction)
                # Time = time
                # Date = date
                # date_name = '-'.join(date.split('/'))
                # Vehicle = real_label
                # location = location_name
                # Image= f'{location}_{date_name}_{time}.jpg'
                # # Image = f'{location}' + f'{date}' + f'{time}'+'.jpg'
                # # Image =  f'{Time}.jpg'

                # # print('location----========================',Image)
                # cv2.imwrite(os.path.join('/media/tdb/0234506b-d37b-419a-9865-f54935d824fb/sarthak_fire_detection/anpr_ocr', 'crop_img', Image), cropped_img)
                # # cv2.imwrite(Image, cropped_img)

                #     #print('table data -----------------------------------------',LPN,Time,Vehicle,Image)

                # conn = None
                # cursor = None
                # try:
                #     if LPN:
                #         conn = mysql.connect()
                #         cursor = conn.cursor(pymysql.cursors.DictCursor)
                #         if cursor.execute("SELECT * FROM ocr_info WHERE LicensePlateNumber=%s",(LPN,)):
                #             # resp = jsonify("not enter duplicate City Name")
                #             # return resp
                #             print("not enter duplicate data")
                #             # print('location===================',location)
                #         else:
                #             sql = "INSERT INTO ocr_info(LicensePlateNumber, time, date,Vehicle,Image,location) VALUES(%s,%s,%s,%s,%s, %s)"
                #             data = (LPN,Time,date,Vehicle,Image,location)
                #             conn = mysql.connect()
                #             cursor = conn.cursor()
                #             cursor.execute(sql, data)
                #             conn.commit()
                #             # print('!!!!!!!!!!!!!!!!!!!!!data Added Successfully !!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # except Exception as e:
                #     print(e)
                # finally:
                #     cursor.close()
                #     conn.close()

                ret, jpeg = cv2.imencode('.jpg', Final_Frame)
                Frame = jpeg.tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + Frame + b'\r\n')


@app.route('/getmodelexpectedoutcomes', methods=['POST'])
@cross_origin()
def add_modelprocessdontexpectedoutcomes():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT expected_outcomes FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addlongitude', methods=['POST'])
@cross_origin()
def add_longitute():
    conn = None
    cursor = None
    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _lognitude = _json['longitude']
        _latitude = _json['latitude']
        if _lognitude and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addlongitude WHERE longitude=%s AND latitude=%s",
                              (_lognitude, _latitude,)):
                resp = jsonify("not enter duplicate Longitute And Latitede")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO addlongitude(longitude,latitude) VALUES(%s, %s)"
                data = (_lognitude, _latitude,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('Record Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getlongitute')
@cross_origin()
def users_getlognitude():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM addlongitude")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updatelatitude', methods=['POST'])
@cross_origin()
def update_updatelatitude():
    conn = None
    cursor = None
    try:
        _json = request.json
        print("kkkkk", _json)
        _id = _json['id']
        _lognitude = _json['longitude']
        _latitude = _json['latitude']
        if _latitude and request.method == 'POST':
            sql = "UPDATE addlongitude SET longitude=%s,latitude=%s WHERE id=%s"
            data = (_lognitude, _latitude, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletelognitude', methods=['POST'])
@cross_origin()
def update_deletelognitude():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        if _id and request.method == 'POST':
            sql = "DELETE FROM addlongitude WHERE id=%s"
            data = (_id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodeladditionalinfo', methods=['POST'])
@cross_origin()
def add_modelmodelmre():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT additional_info FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodelprocess', methods=['POST'])
@cross_origin()
def add_modelprocess():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _model_name = _json['model_name']
        _introduction = _json['introduction']
        _industries = _json['industries']
        print("llll", _industries, _model_name, _introduction)
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT process FROM modeldata WHERE model_name=%s AND industries=%s",
                              (_model_name, _industries)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodelimages', methods=['POST'])
@cross_origin()
def add_id():
    conn = None
    cursor = None

    try:
        print("request ", request.json),
        _json = request.json
        print("request ", _json)
        _industries = _json['industries']
        # _email = _json['email']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _industries and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM model WHERE industries=%s", (_industries,)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchall()
                print(resp)
                return jsonify(resp)
            else:
                resp = jsonify("id not found")
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getuserdata', methods=['POST'])
@cross_origin()
def add_useriddata():
    conn = None
    cursor = None

    try:
        print("gggggggggggggg ", request.json),
        _json = request.json
        print("request ", _json)
        # _ = _json['id']
        _id = _json['id']
        # _password = _json['password']
        # _type= _json['type']
        # validate the received values
        if _id and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM addcamera WHERE id= %s", (_id,)):
                # resp = jsonify("Pls do not enter duplicate Email Id And Password")
                resp = cursor.fetchone()
                return resp
                # print("not enter duplicate data")         
            # else:
            #   sql = "INSERT INTO userlogin(name, email, password, type) VALUES(%s, %s, %s, %s)"
            #   data = (_name, _email, _password, _type,)
            #   conn = mysql.connect()
            #   cursor = conn.cursor()
            #   cursor.execute(sql, data)
            #   conn.commit()
            #   cursor = conn.cursor(pymysql.cursors.DictCursor)
            #   if cursor.execute("SELECT * FROM userlogin WHERE type=%s",(_type,)):
            #       account = cursor.fetchone()
            #       return account
            #   # sql = "SELECT * FROM userlogin WHERE email=%s AND password=%s",(_email, _password,)
            #   # resp = cursor.fetchone()
            #   return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/delete', methods=['POST'])
@cross_origin()
def update_delete():
    conn = None
    cursor = None
    try:
        _json = request.json
        _camD = _json['camD']
        if _camD and request.method == 'POST':
            sql = "DELETE FROM addcamera WHERE camD=%s"
            data = (_camD,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Camera Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletearea', methods=['POST'])
@cross_origin()
def update_deletestatesttecitydeletearedeare():
    conn = None
    cursor = None
    try:
        _json = request.json
        _areaid = _json['areaid']
        if _areaid and request.method == 'POST':
            sql = "DELETE FROM addarea WHERE areaid=%s"
            data = (_areaid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletecity', methods=['POST'])
@cross_origin()
def update_deletestatesttecitydelete():
    conn = None
    cursor = None
    try:
        _json = request.json
        _citiid = _json['citiid']
        if _citiid and request.method == 'POST':
            sql = "DELETE FROM addcities WHERE citiid=%s"
            data = (_citiid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('City Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteuserlist', methods=['POST'])
@cross_origin()
def delete_deleteuserlist():
    conn = None
    cursor = None
    try:
        _json = request.json
        print("json", request.json)
        _id = _json['id']
        print("idid", _id)
        if _id and request.method == 'POST':
            sql = "DELETE FROM adduser WHERE id=%s"
            data = (_id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletestate', methods=['POST'])
@cross_origin()
def update_deletestatestte():
    conn = None
    cursor = None
    try:
        _json = request.json
        _stateid = _json['stateid']
        if _stateid and request.method == 'POST':
            sql = "DELETE FROM addstate WHERE stateid=%s"
            data = (_stateid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('State Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addvids', methods=['POST'])
@cross_origin()
def add_vids():
    conn = None
    cursor = None
    try:
        _json = request.json
        _speed = _json['speed']
        _alert_type = _json['alert']
        _location = _json['location']
        _date = _json['date']
        _vehicle = _json['vehicle']
        _image = _json['image']
        if _location and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            if cursor.execute("SELECT * FROM vids WHERE location=%s", (_location,)):
                resp = jsonify("Duplicate Value Entered")
                return resp
                # print("not enter duplicate data")         
            else:
                sql = "INSERT INTO vids(speed, alert_type, date, vehicle, location, image) VALUES(%s,%s, %s, %s, %s, %s)"
                data = (_speed, _alert_type, _location, _date, _vehicle, _image)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify('New Data Added Successfully!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletecountry', methods=['POST'])
@cross_origin()
def update_deletecountry():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        if _countryid and request.method == 'POST':
            sql = "DELETE FROM addcountry WHERE countryid=%s"
            data = (_countryid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Country Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getarea', methods=['POST'])
@cross_origin()
def update_getarea():
    conn = None
    cursor = None
    try:
        _json = request.json
        _stateid = _json['stateid']
        _citiid = _json['citiid']
        _countryid = _json['countryid']
        if _countryid and request.method == 'POST':
            sql = "SELECT  * FROM addarea WHERE stateid=%s OR countryid=%s AND citiid=%s"
            data = (_stateid, _countryid, _citiid,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            resp = cursor.fetchall()
            conn.commit()
            return jsonify(resp)
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getcity', methods=['POST'])
@cross_origin()
def update_cityid():
    conn = None
    cursor = None
    try:
        _json = request.json
        _stateid = _json['stateid']
        _countryid = _json['countryid']
        if _countryid and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM addcities WHERE stateid=%s AND countryid=%s", (_stateid, _countryid))
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getcountry1', methods=['POST'])
@cross_origin()
def update_getsatecountryeee():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        if _countryid and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM addcountry WHERE countryid=%s", (_countryid))
            rows = cursor.fetchone()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getstate', methods=['POST'])
@cross_origin()
def update_getsate():
    conn = None
    cursor = None
    try:
        _json = request.json
        _countryid = _json['countryid']
        if _countryid and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM addstate WHERE countryid=%s", (_countryid))
            rows = cursor.fetchall()
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deleteuser', methods=['POST'])
@cross_origin()
def io_delete():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        # _id = _json['id']
        _email = _json['email']
        _password = _json['password']
        # _fire = _json['fire']
        # _fall = _json['fall'] 
        # _fight = _json['fight']   
        # validate the received values
        if _email and _password and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "DELETE FROM userlogin WHERE email=%s AND password=%s"
            data = (_email, _password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record Deleted successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getmodels')
@cross_origin()
def users_user():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM models")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# @app.route('/getcountry')
# @cross_origin()
# def users_getcountry():
#     conn = None
#     cursor = None
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("SELECT * FROM addcountry")
#         rows = cursor.fetchall()
#         resp = jsonify(rows)
#         resp.status_code = 200
#         return resp
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close() 
#         conn.close()
@app.route('/getcountry')
@cross_origin()
def users_getcountry():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM addcountry")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getcitylist')
@cross_origin()
def users_getcountrycityerrr():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            " SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid) as countryname ,(SELECT C.statename FROM addstate C WHERE C.stateid=R.stateid) as statename FROM addcities R")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getarealist')
@cross_origin()
def users_getcountrycityerrrcountry():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            " SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid) as countryname ,(SELECT C.statename FROM addstate C WHERE C.stateid=R.stateid) as statename ,(SELECT T.citiname FROM addcities T WHERE T.citiid=R.citiid) as citiname FROM addarea R")
        # cursor.execute("SELECT * FROM addarea")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getstatelist')
@cross_origin()
def users_getcountrycityerrrkkkk():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid) as countryname FROM addstate R")
        # select S.statename from states S where S.stateid=R.state) as statename, (select C.cityname from cities 
        # C where C.cityid=R.city) as cityname  from restaurant R",
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getcountry')
@cross_origin()
def users_getcountryrt5677():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM addcountry")
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getallusers')
@cross_origin()
def users_getalluser():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT DISTINCT email,name,password FROM userlogin WHERE type IN ('useradmin', 'admin')")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getfare', methods=['POST'])
@cross_origin()
def getfare():
    conn = None
    cursor = None

    try:
        _json = request.json
        # _vehicle=_json['Vehicle'] 
        _vid = _json['vid']
        print('fjfjfjfj -------------------------------', _json)
        conn = mysql.connect()
        cursor3 = conn.cursor(pymysql.cursors.DictCursor)
        cursor3.execute("SELECT * FROM vehiclemaster WHERE vid=%s", (_vid,))
        r = cursor3.fetchone()
        _vehicle = r['vehiclename']
        print("vehiclevenamemmmmmmmmmmmmmmmmmmmmm----------------------", _vehicle)
        if _vehicle and request.method == 'POST':
            conn = mysql.connect()
            cursor1 = conn.cursor(pymysql.cursors.DictCursor)
            cursor2 = conn.cursor(pymysql.cursors.DictCursor)
            cursor1.execute("SELECT DISTINCT fare FROM faremaster WHERE vid=%s", (_vid,))
            cursor2.execute("SELECT Vehicle FROM ocr_info WHERE Vehicle=%s", (_vehicle,))
            rows1 = cursor1.fetchall()
            fare = rows1[0]
            fare = fare['fare']
            rows2 = cursor2.fetchall()
            length = len(rows2)
            print(length)
            total_fare = length * fare
            tt = {}
            tt['total_fare'] = total_fare
            tt['total_vehicle'] = length
            resp = jsonify(tt)
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor1.close()
        cursor2.close()
        conn.close()


@app.route('/getallusers1')
@cross_origin()
def users_getalluser1():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM addcamera WHERE showvalue=1")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getuser')
@cross_origin()
def iogetcamera_getuseruser():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM addcamera ")
        # cursor.execute("SELECT * FROM userlogin WHERE type='useradmin'")
        cursor.execute("SELECT * FROM adduser")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getcamera')
@cross_origin()
def iogetcamera_delete():
    conn = None
    cursor = None
    # print('bc =====================================================', bc)
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM addcamera ")
        # cursor.execute("SELECT * FROM userlogin WHERE type='useradmin'")
        # cursor.execute("SELECT * FROM addcamera")
        cursor.execute(
            " SELECT R.*,(SELECT S.countryname FROM addcountry S WHERE S.countryid=R.countryid)"
            " as countryname ,(SELECT C.statename FROM addstate C WHERE C.stateid=R.stateid) as statename ,"
            "(SELECT T.citiname FROM addcities T WHERE T.citiid=R.citiid) as citiname ,"
            "(SELECT Y.areaname FROM addarea Y WHERE Y.areaid=R.areaid) as areaname FROM addcamera R")
        rows = cursor.fetchall()
        print("all camera data", rows)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getvehiclelist')
@cross_origin()
def vehicle_list():
    conn = None
    cursor = None
    # print('bc =====================================================', bc)
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM addcamera ")
        # cursor.execute("SELECT * FROM userlogin WHERE type='useradmin'")
        # cursor.execute("SELECT * FROM addcamera")
        cursor.execute(" SELECT * FROM ocr_info")
        rows = cursor.fetchall()
        print("all lst vehicle data", rows)
        resp = jsonify(rows)
        # print(bc)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# def ocr(_path):

#     # get_path.var = bc
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S %d/%m/%Y") 
#     time = current_time.split(' ')[0]
#     date = current_time.split(' ')[-1]
#     cap = cv2.VideoCapture(_path)
#     while True:
#         ret, frame = cap.read()
#         if ret == True:
#             # print('rows =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', bc)
#             # try:
#             prediction, image_frame = run(frame)
#             LPN = prediction 
#             # print('----------------------------------- prediction  -----------------------------------', prediction)
#             Time = time 
#             Date = date 
#             # Vehicle = labels 
#             Image =  f'{time}.jpg'
#             if request.method == 'POST':
#                 conn = mysql.connect()
#                 cursor = conn.cursor(pymysql.cursors.DictCursor)
#                 # if cursor.execute("SELECT * FROM ocr_info WHERE citiname=%s",(_citiname,)):
#                 #     resp = jsonify("not enter duplicate City Name")
#                 #     return resp
#                 #     # print("not enter duplicate data")         
#                 # else:
#                 sql = "INSERT INTO ocr_info('License Plate Number', 'Time', 'Date',Vehicle,Image) VALUES(%s,%s,%s,%s,%s)"
#                 data = (LPN,Time,date,Vehicle,Image)
#                 conn = mysql.connect()
#                 cursor = conn.cursor()
#                 cursor.execute(sql, data)
#                 conn.commit()
#                 resp = jsonify('Added Successfully!')
#                 resp.status_code = 200
#             # print('bharat -----------------------------------------------------', image_frame)
#             ret, jpeg = cv2.imencode('.jpg', image_frame)
#             Frame=jpeg.tobytes()
#             yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + Frame + b'\r\n')
# except:
#   continue
# else:
#     break
@app.route('/getusersapi')
@cross_origin()
def getusersapi():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # cursor.execute("SELECT * FROM addcamera ")
        # cursor.execute("SELECT * FROM userlogin WHERE type='useradmin'")
        cursor.execute("SELECT DISTINCT email,name,password FROM userlogin WHERE type IN ('useradmin')")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getshowvalue')
@cross_origin()
def showvalue():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM addcamera WHERE showvalue=1")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/updaterstp', methods=['POST'])
@cross_origin()
def upd_rstp():
    conn = None
    cursor = None
    try:
        print("l ", request.json),
        _json = request.json
        _name = _json['name']
        _rstp = _json['rstp']
        print("p", _rstp)
        # _fire = _json['fire']
        # _fall = _json['fall'] 
        # _fight = _json['fight']   
        # validate the received values
        if _rstp and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE addcamera SET rstp=%s, name=%s WHERE rstp=%s"
            data = (_rstp, _name, _rstp,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Camera  Updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update_show', methods=['POST'])
@cross_origin()
def update_show():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        _showvalue = _json['showvalue']
        # _rstp = _json['rstp']
        # _fire = _json['fire']
        # _fall = _json['fall'] 
        # _fight = _json['fight']   
        # validate the received values
        if _showvalue and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE value SET showvalue=%s"
            data = (_showvalue,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            cursor.execute("UPDATE addcamera SET showvalue=0")
            cursor.execute("UPDATE addcamera SET showvalue1=0")
            cursor.execute("UPDATE addcamera SET showvalue1=1 WHERE id=%s", (_showvalue,))
            conn.commit()
            resp = jsonify('Models updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/handleall2', methods=['POST'])
@cross_origin()
def update_all2():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        _showvalue = _json['showvalue']
        if _showvalue and request.method == 'POST':
            sql = "UPDATE value SET showvalue=%s"
            data = (_showvalue,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            cursor.execute("UPDATE addcamera SET showvalue1=0")
            cursor.execute("UPDATE addcamera SET showvalue=0")
            conn.commit()
            resp = jsonify('Models updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addpath', methods=['POST'])
@cross_origin()
def addpath():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        # _rstp = _json['rstp']
        # _fire = _json['fire']
        # _fall = _json['fall'] 
        # _fight = _json['fight']   
        # validate the received values
        if request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            # sql = "UPDATE value SET showvalue=%s"
            # data = (_showvalue,)
            # conn = mysql.connect()
            # cursor = conn.cursor()
            # cursor.execute(sql, data)
            # cursor.execute("UPDATE addcamera SET showvalue=0")
            # conn.commit()
            resp = jsonify('Models updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/handleallcameras', methods=['POST'])
@cross_origin()
def updateallcamrad():
    conn = None
    cursor = None
    try:
        print("lala ", request.json),
        _json = request.json
        _showvalue = _json['showvalue']
        # _rstp = _json['rstp']
        # _fire = _json['fire']
        # _fall = _json['fall'] 
        # _fight = _json['fight']   
        # validate the received values
        if _showvalue and request.method == 'POST':
            # do not save password as a plain text
            # _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE value SET showvalue=%s"
            data = (_showvalue,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            cursor.execute("UPDATE addcamera SET showvalue1=0")
            cursor.execute("UPDATE addcamera SET showvalue=1 WHERE id=%s", (_showvalue,))
            conn.commit()
            resp = jsonify('Models updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/getvehiclemaster')
@cross_origin()
def getvehiclemater():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(" SELECT * FROM vehiclemaster")
        rows = cursor.fetchall()
        print("all camera data", rows)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/video_feed', methods=['GET'])
@cross_origin()
def video():
    lis, loc = get_path()
    # for i in lis:
    # # j=jsonify(path)
    #     # print('pat ---------------------------------------------------------', path)

    # # return j
    return Response(ocr(lis, loc), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print('')
    app.run(debug=True)


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()

# path = '/home/hp/Documents/fall.png'

# file_name = path.split('/')[-1].split('.')[0]
# files = glob.glob(os.path.join(os.getcwd(), 'backend_folder', '*.png'))
# for file in files:
#   if file.split('/')[-1].split('.')[0] == file_name:
#       img = cv2.imread(path)
#       cv2.imshow('test', img)
#       cv2.waitKey(0)
#       cv2.destroyAllWindows()
#       print(f'img -- {file}')


# @app.route("/<section>")
# def data(section):
#     assert section == request.view_args['section']
#     print('bharat -----------------------------------------------------------', section)
#     return section

# path = '/home/hp/Documents/fall.png'

# file_name = path.split('/')[-1].split('.')[0]
# files = glob.glob(os.path.join(os.getcwd(), 'backend_folder', '*.png'))
# for file in files:
#   if file.split('/')[-1].split('.')[0] == file_name:
#       img = cv2.imread(path)
# cv2.imshow('test', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(f'img -- {file}')
