from MapLocator_LatLong import MapLocatorLatLong
from MapLocator_State import MapLocatorState

def main():
    command = ''
    print('\n\nWelcome to USGS Map Downloader\n')
    while True:
        print('Menu:')
        print('  1) Download from Lat Long')
        print('  2) Download a state')
        print('  3) Exit\n')
        command = input('  Enter 1 or 2 based on your choice: ')
        
        if command == '1':
            MapLocatorLatLong()
        elif command == '2':
            MapLocatorState()
        elif command == '3':
            exit()
        else:
            print('Choose 1, 2, or 3')


if __name__ == '__main__':
    main()