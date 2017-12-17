from os import (path, environ)
from glob import glob

GOOGLE_USER_DATA = path.join(environ['LOCALAPPDATA'],
	'Google', 'Chrome', 'User Data')

def chrome_profile_join(*args):
	o = glob(GOOGLE_USER_DATA+'\Profile *')
	o.append(GOOGLE_USER_DATA+'\Default')
	return (path.join(i, *args) for i in o)