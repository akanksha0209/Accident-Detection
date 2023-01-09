import time
import cv2
import requests
from googleplaces import GooglePlaces, types, lang
import requests
import json
from flask import Flask, render_template, url_for, flash, redirect, Response
from datetime import datetime
from flask_bootstrap import Bootstrap
from camera import Camera
from ip_address import get_ip_address
# from location_hospital import get_location

app = Flask(__name__)
camera = Camera()
# API_KEY = 'AIzaSyBPNgFZT6ZUIN2Wsrk3GOSgo67NAKseTIA'
# google_places = GooglePlaces(API_KEY)



def gen():
    while True:
        frame = camera.startapplication()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/accident_page')
def accident_page():
    global ip_address, lat, lon, query_result
    lat=None
    lon=None
    if (camera.prob).any() > 95:
        response = requests.post("http://ip-api.com/batch", json=[
            {"query": "208.80.152.201"},

        ]).json()

        for ipinfo in response:
            lat = ipinfo['lat']
            lon = ipinfo['lon']
        # query_result = google_places.nearby_search(
        #
        #     lat_lng={'lat': lat, 'lng': lon},
        #     radius=5000,
        #
        #     types=[types.TYPE_HOSPITAL])
        #
        # if query_result.has_attributions:
        #     print(query_result.html_attributions)

    return render_template('accident_page.html',probability=camera.prob,  ip_address_lat=lat,
                           ip_address_lon=lon,)


if __name__ == '__main__':
    app.run(debug=True)





