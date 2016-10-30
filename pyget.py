###################################################################
##
##   COMS3200 Assignment at UQ
##   Must be able to retrieve files with
##   ftp:// or http:// prefix.
##
##   Example files to grab:
##   http://www.itee.uq.edu.au/filething/get/2646/phone-grey.png
##   ftp://ftp.marine.csiro.au/pub/spencer_gulf/met/README
##
###################################################################

import sys
from ftplib import FTP
from urllib.parse import urlparse
from urllib.request import urlopen
from requests import get

"""
    Go and get our file using the ftp library
    provided by python3.
"""
def getFtpFile(urlPased, fileGet):
    print('Getting your ftp file...')
    #make ftp connection, set as passive by default
    try:
        ftp = FTP(urlParsed.netloc)
    except Exception as e:
        #server we tried to connect to didn't work
        print("Error: Cannot resolve \""+urlParsed.netloc+"\"\nEnding..")
        return

    try:
        ftp.login('anonymous')
    except Exception as e:
        print("Error connecting: " + str(e) + "\nEnding...")
        return

    print("Connected successfully...")
    #check to see if we need to find the sub dir
    if (len(pathSections)>2):
        print("Need to change directories...")
        subfolders = pathSections[1:-1]
        # For each folder in the path to the file
        for folder in subfolders:
            current = []
            print("Checking for directory " + folder)
            try:
                ftp.retrlines('LIST', current.append)
            except Exception as e:
                print("Error retrieving lines\nEnding..")
                ftp.quit()
                return
            # Is that folder a name of any of the files in this directory
            if (any(folder in fileList for fileList in current)):
                #found it, move in
                ftp.cwd(folder)
                print("212: Moved to directory " + folder)
            else:
                print("That directory doesnt exist!\nEnding...")
                ftp.quit()
                return

    # Populate a list with the contents of the current directory
    files = []
    ftp.retrlines('LIST', files.append)
    # Check to see if our file exists on the server
    print("Checking if file exists...")
    if (any(fileGet in s for s in files)):
        print("Found " + fileGet + "!\nDownloading now...")
        try:
            ftp.retrbinary('RETR '+fileGet, open(fileGet, 'wb').write)
            print("216: Successfully saved " + fileGet)
            ftp.quit()
        except Exception as e:
            print("Error: " + str(e))
            ftp.quit()
            return
    else:
        # Trouble getting the file, might not be there, or permissions
        print("550: Requested action not taken. File unavailable, not found, not accessible")
        ftp.quit()

"""
    Using the requests library download an http based
    file to our directory that the program is executed
    from.
"""
def getHttpFile(url, fileGet):
    print("Connecting...")
    try:
        req = get(url)
        print("Connected successfully...")
        fi = open(fileGet,'wb')
        fi.write(req.content)
        print(fileGet + " was written successfully!")
    except Exception as e:
        print("Could not connect, check the url.")

"""
    Execute our functions depending on whether we are
    dealing with an ftp or http based connection.
"""
if __name__ == "__main__":
    #extract the arg passed to program
    url = sys.argv[1]
    #urlparse turns our url into sections to deal with
    urlParsed = urlparse(url)
    #.path on our url extracts everything after the url
    pathSections = urlParsed.path.split('/')
    #the last element of our array is the actual file name
    fileGet = pathSections[-1]
    if (urlParsed.scheme == 'http'):
        getHttpFile(url, fileGet)
    elif (urlParsed.scheme == 'ftp'):
        getFtpFile(urlParsed, fileGet)
    else:
        print("Usage: python3[.5] pyget.py ftp://[path_to_file] | http://[path_to_file]")