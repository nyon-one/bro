from browser_cookie3 import firefox
from requests import Session
from bs4 import BeautifulSoup

from urllib.parse import urlparse, parse_qs, ParseResult
from http.cookiejar import LWPCookieJar
from ..rel import Rel


class LocalCookie(LWPCookieJar):
	def __init__(self, file_name):
		file_name = Rel(__file__).folder('.cook').join(file_name)
		LWPCookieJar.__init__(self, file_name)

	def isempty(self):
		return len(self) == 0

class SessionX(Session):
	PARSER = 'html.parser'
	def _soup(self, content, **kwargs):
		return BeautifulSoup(content, self.PARSER, **kwargs)

	def clean_soup(self, soup, select=None):
		if not select:
			select = 'script'
		for e in soup.select(select):
			# s.extract()
			e.decompose()

	def parse_url(self, url):
		class Url(object):
			def __init__(self, url):
				self.url = urlparse(url)
				self.querys = parse_qs(self.url.query)

			def get(self, key):
				values = self.querys.get(key, [])
				if len(values)==1:
					return values.pop()
				return values
		return Url(url)

	def send(self, request, **kwargs):
		r = super().send(request, **kwargs)
		r.soup = self._soup(r.text)
		return r

	def html(self, url, **kwargs):
		return self.get(url, **kwargs).soup

class Bro(SessionX):
	USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
	HEADERS = {}
	def __init__(self, *args, **kwargs):
		SessionX.__init__(self, *args, **kwargs)
		self.headers['user-agent'] = self.USER_AGENT
		self.headers.update(self.HEADERS)

class MobBro(Bro):
	USER_AGENT = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'

class Bot(Bro):
	USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

class Firefox(Bro):
	USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
	def __init__(self, *args, **kwargs):
		Bro.__init__(self, *args, **kwargs)
		self.cookies = firefox()

from cfscrape import CloudflareScraper

class Cf(CloudflareScraper, SessionX):pass