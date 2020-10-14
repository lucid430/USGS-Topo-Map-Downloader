import csv
import os
import sys
import requests
from pathlib import Path

MAPS_FILE = 'topomaps_all_lat_long.csv'
lat = 0.0
lon = 0.0

def DownloadFile(url, filename):
    scriptPath = sys.path[0]
    folder = './LatLong/'
    r = requests.get(url)
    with open(folder + filename, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

# Case where user wants to download all maps
def FindDownloadMap(MAPS_FILE, latLong):
    with open(MAPS_FILE) as csvfile:
        next(csvfile)
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            northLat = row[0]
            southLat = row[2]
            eastLong = row[1]
            westLong = row[3]
            if(LatLongWithinBox(northLat, southLat, eastLong, westLong, latLong[0], latLong[1])):
                url = row[4]
                filename = url.split('/')[-1]
                print('Downloading: ' + filename, end='')
                DownloadFile(url, filename)
                print('*')

def LatLongWithinBox(nlim, slim, elim, wlim, lat, lon):
    #Lat must be within North Limit and South Limit
    if(lat < nlim and lat > slim):
        #lon must be within east and west limit
        if(lon < elim and lon > wlim):
            return True
    return False

def GetLatLong():
    lat = float(input('Input Latitude rounded to 2 decimals'))
    lon = float(input('Input Longitude rounded to 2 decimals'))
    latlong = [lat, lon]
    return latlong

latLong = GetLatLong()  
FindDownloadMap(MAPS_FILE, latLong)
