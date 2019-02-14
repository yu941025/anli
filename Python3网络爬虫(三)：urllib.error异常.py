__author__ = 'Administrator'
'''from urllib import request
from urllib import error
if __name__=='__main__':
    url="http://www.douyu.com/Jack_Cui.html"
    req=request.Request(url)
    try:
        response=request.urlopen(req)
        html=response.read().decode('utf-8')
    except error.HTTPError as e:
        print(e.code)

    except error.URLError as e :
        print(e.reason)
        print(e)'''

from urllib import request
from urllib import error
if __name__=='__main__':
    url='http://www.douyu.com/Jack_Cui.html'
    req=request.Request(url)
    try:
        aa=request.urlopen(req)
        html=aa.read().decode('utf-8')
    except error.HTTPError as e:
        if hasattr(e,'code'):
            print(e.code)
    except error.URLError as e :
        if hasattr(e,'reason'):
            print(e.reason)