"""
About:
Python wrapper for the New York Times Archive API
https://developer.nytimes.com/article_search_v2.json
"""
from newsapi.articles import Articles
import sys,json
import requests

key = '522497f7b4b940b7946eeed6909ed817'
params = {}
api = Articles(API_KEY=key)
reload(sys)
sys.setdefaultencoding('utf8')


class APIKeyException(Exception):
    def __init__(self, message): self.message = message


class InvalidQueryException(Exception):
    def __init__(self, message): self.message = message


class ArchiveAPI(object):
    def __init__(self, key=None):
        self.key = key
        self.root = 'http://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}'
        if not self.key:
            nyt_dev_page = 'http://developer.nytimes.com/docs/reference/keys'
            exception_str = 'Warning: API Key required. Please visit {}'
            raise APIKeyException(exception_str.format(nyt_dev_page))

    def query(self, year=None, month=None, key=None, ):
        if not key: key = self.key
        if (year < 1882) or not (0 < month < 13):
            # currently the Archive API only supports year >= 1851
            exception_str = 'Invalid query: See http://developer.nytimes.com/archive_api.json'
            raise InvalidQueryException(exception_str)
        url = self.root.format(year, month, key)
        print url
        r = requests.get(url)
        return r.json()

years = [2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
api = ArchiveAPI('522497f7b4b940b7946eeed6909ed817')
for year in years:
    for month in months:
        mydict = api.query(year, month)
        file_str = './data/nytimes' + str(year) + '-' + '{:02}'.format(
            month) + '.json'
        with open(file_str, 'w') as fout:
            json.dump(mydict, fout)
        fout.close()


