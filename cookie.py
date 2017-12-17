from http.cookiejar import LWPCookieJar
from ..rel import Rel
from . import Bro, SessionX

class LocalCookie(LWPCookieJar):
	def __init__(self, file_name):
		file_name = Rel(__file__).folder('.cook').join(file_name)
		LWPCookieJar.__init__(self, file_name)

	def isempty(self):
		return len(self) == 0

from browser_cookie3 import firefox

class Firefox(Bro):
	USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
	def __init__(self, *args, **kwargs):
		Bro.__init__(self, *args, **kwargs)
		self.cookies = firefox()

from cfscrape import CloudflareScraper

class Cf(CloudflareScraper, SessionX):pass