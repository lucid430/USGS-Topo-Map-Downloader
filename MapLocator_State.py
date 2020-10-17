LIST_STATES = {  
    'AL',
    'AK',
    'AZ',
    'AR',
    'CA',
    'CO',
    'CT',
    'DC',
    'DE',
    'FL',
    'GA',
    'HI',
    'ID',
    'IL',
    'IN',
    'IA',
    'KS',
    'KY',
    'LA',
    'ME',
    'MD',
    'MA',
    'MI',
    'MN',
    'MS',
    'MO',
    'MT',
    'NE',
    'NV',
    'NH',
    'NJ',
    'NM',
    'NY',
    'NC',
    'ND',
    'OH',
    'OK',
    'OR',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VT',
    'VA',
    'WA',
    'WV',
    'WI',
    'WY'
}
MAP_STATES = {
    'ALABAMA'           : 'AL',
    'ALASKA'            : 'AK',
    'ARIZONA'           : 'AZ',
    'ARKANSAS'          : 'AR',
    'CALIFORNIA'        : 'CA',
    'COLORADO'          : 'CO',
    'CONNECTICUT'       : 'CT',
    'DELAWARE'          : 'DE',
    'FLORIDA'           : 'FL',
    'GEORGIA'           : 'GA',
    'HAWAII'            : 'HI',
    'IDAHO'             : 'ID',
    'ILLINOIS'          : 'IL',
    'INDIANA'           : 'IN',
    'IOWA'              : 'IA',
    'KANSAS'            : 'KS',
    'KENTUCKY'          : 'KY',
    'LOUISIANA'         : 'LA',
    'MAINE'             : 'ME',
    'MARYLAND'          : 'MD',
    'MASSACHUSETTS'     : 'MA',
    'MICHIGAN'          : 'MI',
    'MINNESOTA'         : 'MN',
    'MISSISSIPPI'       : 'MS',
    'MISSOURI'          : 'MO',
    'MONTANA'           : 'MT',
    'NEBRASKA'          : 'NE',
    'NEVADA'            : 'NV',
    'NEWHAMPSHIRE'      : 'NH',
    'NEWJERSEY'         : 'NJ',
    'NEWMEXICO'         : 'NM',
    'NEWYORK'           : 'NY',
    'NORTHCAROLINA'     : 'NC',
    'NORTHDAKOTA'       : 'ND',
    'OHIO'              : 'OH',
    'OKLAHOMA'          : 'OK',
    'OREGON'            : 'OR',
    'PENNSLYVANIA'      : 'PA',
    'RHODEISLAND'       : 'RI',
    'SOUTHCAROLINA'     : 'SC',
    'SOUTHDAKOTA'       : 'SD',
    'TENNESEE'          : 'TN',
    'TEXAS'             : 'TX',
    'UTAH'              : 'UT',
    'VERMONT'           : 'VT',
    'VIRGINIA'          : 'VA',
    'WASHINGTON'        : 'WA',
    'WESTVIRGINIA'      : 'WV',
    'WISCONSIN'         : 'WI',
    'WYOMING'           : 'WY',
    'WASHINGTONDC'      : 'DC'
}
MAPS_FILE = 'topomaps_all.csv'
MAPS_FILE_TEST = 'topomaps_test.csv'

TOTAL_FILE_SIZE_BYTES = 0

from pathlib import Path
import sys
import getopt
import requests
import os
import csv
import progressbar
import time
import numpy as np

# Expect: User will enter: 
#               py TopoDownloader.py -s Ohio
#                   or
#               py TopoDownloader.py -s OH
#                   or
#               py TopoDownloader.py -s all

#######################################################################################
#######################################################################################

# Take a full state name and convert it to two letter shorthand
def ConvertToShorthand(state):
    return MAP_STATES.get(state.upper())

# Using getopt library, collect a list of states from user input
# Returns: List of states - either 
def GetStates():
    argv = sys.argv[1:]
    states = []
    try:
        opts, args = getopt.getopt(argv, 's', ['state'])
        print('States selected: ', end='')
        for state in args:

            if(len(state) > 3 and state.upper() != 'ALL'):
                states.append(ConvertToShorthand(state))

            elif(state.upper() != 'ALL'):
                state = state.upper()
                states.append(state)

            else:
                states.append('ALL')

    except getopt.GetoptError:
        print('MESSUP')

    print(states)
    return states

#######################################################################################
#######################################################################################
def GetState():
    state = input('  Enter a state: ')
    stateAry = []
    if(len(state) > 3 and state.upper() != 'ALL'):
        stateAry.append(ConvertToShorthand(state))

    elif(state.upper() != 'ALL'):
        state = state.upper()
        stateAry.append(state)

    else:
        stateAry.append('ALL')

    print('  You chose ' + state + '.')

    return stateAry
#######################################################################################
#######################################################################################

# Create folders of states
def CreateFolders(states):
    if(states[0] == 'ALL'):
        for state in LIST_STATES:
            #os.mkdir(state)
            os.makedirs(state, exist_ok=True)
    else:
        for state in states:
            #os.mkdir(state)
            os.makedirs(state, exist_ok=True)



#######################################################################################
#######################################################################################

# https://prd-tnm.s3.amazonaws.com/StagedProducts/Maps/USTopo/PDF/AK/AK_Talkeetna_D-3_NE_20140102_TM_geo.pdf
# Column 9 in csv

# def DownloadFile(state, url, filename):
#     scriptPath = sys.path[0]
#     downloadPath = Path(scriptPath + '/' + state + '/')
#     folder = './' + state + '/'
#     r = requests.get(url)
#     with open(folder + filename, 'wb') as file:
#         response = requests.get(url)
#         file.write(response.content)

def DownloadFile(state, url, filename, n_chunk=1):
    request = requests.get(url, stream=True)

    # Estimates the number of bar updates
    block_size = 10*1024*1024
    file_size = int(request.headers.get('Content-Length', None))
    num_bars = np.ceil(file_size / (n_chunk * block_size))
    bar = progressbar.ProgressBar(maxval=num_bars).start()

    # Create folder for file
    folder = './' + state + '/'
    os.makedirs(folder, exist_ok=True)

    with open(folder + filename, 'wb') as file:
        for i, chunk in enumerate(request.iter_content(chunk_size=n_chunk * block_size)):
            file.write(chunk)
            bar.update(i+1)
            # Sleep to see bar progress
            time.sleep(0.05)
        #file.write(request.content)



#######################################################################################
#######################################################################################

def PrintStartDownload():
    print('                                        ')
    print('---------Begin Downloading Maps---------')
    print('---DONT STOP THE SCRIPT WHILE RUNNING---')
    print('----------------------------------------')
    print('\n')

def PrintEndDownload():
    print('\n')
    print('----------------------------------------')
    print('-----------Done Downloading-------------')

def PrintTotalDownloadSize():
    global TOTAL_FILE_SIZE_BYTES
    totalsize = ConvertByteToGigabyte(TOTAL_FILE_SIZE_BYTES)
    print('\n' + 'Total Download Size: ' + totalsize)

def ConvertByteToMegabyte(filesize):
    filesize = int(filesize)
    mbsize = round((filesize/(1024*1024)), 1)
    return str(mbsize) + 'MB'

def ConvertByteToGigabyte(total_file_size):
    total_file_size = int(total_file_size)
    gbsize = round((total_file_size/(1024*1024*1024)), 1)
    return str(gbsize) + 'GB'
# Case where user wants to download from specific states
def DownloadMaps(MAPS_FILE, states):
    PrintStartDownload()
    with open(MAPS_FILE) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            state = row[2]
            url = row[9]
            filesizeBytes = row[11]
            if(state in states):
                filesize = ConvertByteToMegabyte(filesizeBytes)
                filename = url.split('/')[-1]
#                DownloadFile(state, url, filename)
                print('*\t' + filesize)
                
                global TOTAL_FILE_SIZE_BYTES
                TOTAL_FILE_SIZE_BYTES += int(filesizeBytes)

    PrintEndDownload()



# Case where user wants to download all maps
def DownloadAllMaps(MAPS_FILE):
    PrintStartDownload()
    with open(MAPS_FILE) as csvfile:
        next(csvfile)
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            state = row[2]
            url = row[9]
            filename = url.split('/')[-1]
            filesizeBytes = row[11]
            filesize = ConvertByteToMegabyte(filesizeBytes)

            print('Downloading: ' + filename, end='')
            DownloadFile(state, url, filename)
            print('*\t' + filesize)

            global TOTAL_FILE_SIZE_BYTES
            TOTAL_FILE_SIZE_BYTES += int(filesizeBytes)
    PrintEndDownload()

#######################################################################################
#######################################################################################

def MapLocatorState():
#    stateAry = GetStates()
    stateAry = GetState()
    # CreateFolders(states)
    CreateFolders(stateAry)
    if(stateAry[0] == 'ALL'):
        DownloadAllMaps(MAPS_FILE)
    else:
        DownloadMaps(MAPS_FILE, stateAry)
    PrintTotalDownloadSize()
    #ReadMapsFile(MAPS_FILE, states)