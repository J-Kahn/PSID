import requests
import lxml.html
import os
import os.path
import zipfile
import sas
import gc

# Keep track of starting directory for convenience
start_dir       = os.getcwd()

target_dir      = '/home/PSID' # Enter the directory you want the PSID files in
user            = '' # Enter your user name, you must register at psidonline.isr.umich.edu
password        = '' # Enter associated password
login_url       = 'http://simba.isr.umich.edu/u/Login.aspx' # Logi url

# Make target directory if it does not exist
if not os.path.exists(target_dir):
	
	os.makedirs(target_dir)


# Go to target directory
os.chdir(target_dir)

# Start request session and go to login URL
session         = requests.session()

# Get out VIEWSTATE and EVENTVALIDATION variables
start           = session.get(login_url)
html            = start.text
root            = lxml.html.fromstring(html)

EVENTVALIDATION = root.xpath('//input[@name="__EVENTVALIDATION"]')[0].attrib['value']
VIEWSTATE       = root.xpath('//input[@name="__VIEWSTATE"]')[0].attrib['value']

acc_pwd         = {	'ctl00$ContentPlaceHolder1$Login1$UserName'    : user,
					'ctl00$ContentPlaceHolder1$Login1$Password'    : password,
					'ctl00$ContentPlaceHolder1$Login1$LoginButton' : 'Log In' ,
					'__EVENTTARGET'                                : '',
					'__EVENTARGUMENT'                               : '',
					'__VIEWSTATE'                                  : VIEWSTATE,
					'__EVENTVALIDATION'                           : EVENTVALIDATION
				}

# Send login message to PSID site
session.post(login_url, data=acc_pwd)

# Check for login
z=session.get('http://simba.isr.umich.edu/data/data.aspx')
tf2 = 'Logout' in z.content
print 'Successful login: ' + str(tf2)

# File years, numbers and labels

file_year       = range(1968,1998) + range( 1999 , 2012, 2 ) 
request_numbers = [1056 ] + range(1058,1083) +  range(1047,1052) + [1040, 1052 , 1132 , 1139 , 1152 , 1156] 
request_start   = 'http://simba.isr.umich.edu/Zips/GetFile.aspx?file='
file_start      = 'FAM'

# Function to download PSID zip file
def download_psid(number, local_filename, sessions):

	# Get the file using requests
	r = sessions.get(request_start + number, stream=True)

	with open(local_filename, 'wb') as f:

		#Write it out in chunks incase it's big
		for chunk in r.iter_content(chunk_size=1024):

			if chunk: 
				f.write(chunk)
				f.flush()

	return local_filename

# Extracting PSID using psid_unzip. Extractall will also extract STATA .do files, etc.
def psid_unzip(filename, extractall = False):

	zfile = zipfile.ZipFile(filename)

	for name in zfile.namelist():

		# Only take out the files we want
		if '.sas' in name or '.txt' in name or '.pdf' in name or extractall == True:

			(dirname, filename) = os.path.split(name)

			if '.pdf' in name:
				dirname = dirname + "Codebooks" # Different directory for Codebooks
			if '.txt' in name:
				nascii = name # Keep track of ascii name
			if '.sas' in name:
				nsas   = name # Keep track of sas name

			print "Decompressing " + filename + " on " + dirname
				
			if not dirname == '':

				if not os.path.exists(dirname):

					os.makedirs(dirname)

			zfile.extract(name, dirname) # Extract file

	return (nsas, nascii)

for i in range(0,len(request_numbers)):

	print 'PSID year: ' + str(file_year[i])
	file_name = file_start + str(file_year[i]) + '.zip'

	# Grab file
	x = download_psid(str(request_numbers[i]), file_name, session)
	
	print "Downloaded"
	
	# Unzip
	nsas, nascii = psid_unzip(file_name)
	
	print "Unzipped"

	# Turn it into a .csv
	sas.sas_to_csv(nsas, nascii, file_start + str(file_year[i]) + '.csv')

	print "Converted to CSV"

	# Cleanup
	os.remove(nsas)
	os.remove(nascii)
	os.remove(file_name)
	
	print "Deleted"
	gc.collect()


os.chdir(start_dir)