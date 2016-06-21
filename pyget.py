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
	#make ftp connection, set as passive by default
	try:
		ftp = FTP(urlParsed.netloc)
	except Exception as e:
		#server we tried to connect to didn't work
		print("ERROR:> Cannot resolve \""+urlParsed.netloc+"\"")
	try:
		ftp.login('anonymous','coms3200@uq.edu.au')
		print('Connected successfully...')
		#check to see if we need to find the sub dir
		if (len(pathSections)>2):
			print("Need to change directories...")
			directsToFile = pathSections[1:-1]
			#for each folder in the path to the file
			for folder in directsToFile:
				currentDir = []
				print('Checking for directory '+folder)
				ftp.retrlines('LIST', currentDir.append)
				#is that folder a name of any of the files in this directory
				if (any(folder in fileList for fileList in currentDir)):
					#found it, move in
					ftp.cwd(folder)
					print("212: Moved to directory "+folder)
				else:
					#does not exist
					print("That directory doesnt exist!")
					ftp.quit()
					return
		#populate a list with the contents of the current dir
		files = []
		ftp.retrlines('LIST', files.append)
		#check to see if our file exists on the server
		print('Checking if file exists...')
		if (any(fileGet in s for s in files)):
			print('Found '+fileGet+"!")
			print('Downloading now...')
			ftp.retrbinary('RETR '+fileGet, open(fileGet, 'wb').write)
			print('216: Successfully saved '+fileGet)
			ftp.quit()
		else:
			#our file does not exist on the server
			print('550: Requested action not taken. File unavailable, not found, not accessible')
			ftp.quit()
	except Exception as e:
		#catch any exception and print it out
		print(str(e))
	
"""
	Using the requests library download an http based
	file to our directory that the program is executed
	from.
"""
def getHttpFile(url, fileGet):
	print('Getting your http file...')
	print('Connecting...')
	req = get(url)
	print('Connected successfully...')
	#open a file to write binary
	fi = open(fileGet,'wb')
	#write the contents of the url we connected to
	fi.write(req.content)
	print(fileGet + ' written successfully!')

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
		print('i dont understand that protocol')
