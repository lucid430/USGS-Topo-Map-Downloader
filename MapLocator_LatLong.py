import csv
import os
import sys
import requests
import progressbar
import time
import numpy as np
from pathlib import Path

MAPS_FILE = 'topomaps_latlong.csv'
lat = 0.0
lon = 0.0

# def DownloadFile(url, filename):
#     scriptPath = sys.path[0]
#     folder = './LatLong/'
#     os.makedirs(folder, exist_ok=True)
#     r = requests.get(url)
#     with open(folder + filename, 'wb') as file:
#         response = requests.get(url)
#         file.write(response.content)

def DownloadFile(url, filename, n_chunk=1):
    request = requests.get(url, stream=True)

    # Estimates the number of bar updates
    block_size = 10*1024*1024
    file_size = int(request.headers.get('Content-Length', None))
    num_bars = np.ceil(file_size / (n_chunk * block_size))
    bar = progressbar.ProgressBar(maxval=num_bars).start()

    # Create folder for file
    folder = './LatLong/'
    os.makedirs(folder, exist_ok=True)

    with open(folder + filename, 'wb') as file:
        for i, chunk in enumerate(request.iter_content(chunk_size=n_chunk * block_size)):
            file.write(chunk)
            bar.update(i+1)
            # Sleep to see bar progress
            time.sleep(0.05)
        #file.write(request.content)


# Case where user wants to download all maps
def FindDownloadMap(MAPS_FILE, latLong):
    with open(MAPS_FILE) as csvfile:
        next(csvfile)
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows: 
            northLat = float(row[0])
            westLong = float(row[1])
            southLat = float(row[2])
            eastLong = float(row[3])
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
    lat = float(input('Input Latitude  (decimal):\t'))
    lon = float(input('Input Longitude (decimal):\t'))
    latlong = [lat, lon]
    print(latlong)
    return latlong

def MapLocatorLatLong():
    latLong = GetLatLong()
    FindDownloadMap(MAPS_FILE, latLong)
