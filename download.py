import requests
import lxml.html
import os
import os.path
import zipfile

start_dir       = os.getcwd()
target_dir      = '/home/PSID'
user            = ''
password        = ''
login_url       = 'http://simba.isr.umich.edu/u/Login.aspx'

os.chdir(target_dir)

session         = requests.session()

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

session.post(login_url, data=acc_pwd)

z=session.get('http://simba.isr.umich.edu/data/data.aspx')
tf2 = 'Logout' in z.content
print 'Successful login: ' + str(tf2)


file_year       = range(1968,1998) + range( 1999 , 2012, 2 )
request_numbers = [1056 ] + range(1058,1082) + [1040, 1052 , 1132 , 1139 , 1152 , 1156]
request_start   = 'http://simba.isr.umich.edu/Zips/GetFile.aspx?file='
file_start      = 'dat'

def download_psid(number, local_filename, sessions):
	r = sessions.get(request_start + number, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()
	return local_filename

def zip_unzip(filename):
	zfile = zipfile.ZipFile(filename)
	for name in zfile.namelist():
		(dirname, filename) = os.path.split(name)
		print "Decompressing " + filename + " on " + dirname
		if not dirname == '':
			if not os.path.exists(dirname):
				os.makedirs(dirname)
	zfile.extract(name, dirname)
#try: 
for i in range(0,len(request_numbers)):
	print str(file_year[i])
	file_name = file_start + str(file_year[i])

	x = download_psid(str(request_numbers[i]), file_name, session)
	print "Downloaded"
	zip_unzip(file_name)
	print "Unzipped"

	os.remove(file_name)
	print "Deleted"

os.chdir(start_dir)

#except:
#	os.chdir(start_dir)