try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pycurl
import lxml.html as lh
import os
from time import sleep
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class webpage(object):
    def __init__(self,url="www.example.com",automator=False):
        self.doc = ""
        self._url = url
        self.data = ''
        self.buffer = StringIO()
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.COOKIEJAR, 'cookie.txt')
        self.curl.setopt(self.curl.COOKIEFILE, 'cookie.txt')
        self.curl.setopt(self.curl.URL, url)
        self.curl.setopt(self.curl.WRITEDATA, self.buffer)
        self.curl.setopt(self.curl.FOLLOWLOCATION, 1)
        self.curl.setopt(self.curl.VERBOSE, 0)
        self.curl.setopt(self.curl.ENCODING, 'gzip, deflate')
        self.curl.setopt(self.curl.HTTPHEADER, ['User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',\
                                          'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                                          'Accept-Language: en-US,en;q=0.5',\
                                          'Connection: keep-alive'])
        self.curl.setopt(self.curl.NOSIGNAL, 0)
        if automator:
            display = Display(visible=0, size=(800, 600))
            display.start()
            driver = webdriver.Firefox()
            driver.get(url)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(.25)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(.25)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(.25)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(.25)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(2)
            data = driver.page_source
            driver.quit()
            display.stop()
            self.fromstring(data,url)


    def xpath(self,path):
        return self.doc.xpath(path)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self,value):
        self._url = value
        self.curl.setopt(self.curl.URL, self._url)

    def post(self,data):
        self.curl.setopt(self.curl.POST, 1)
        self.curl.setopt(self.curl.POSTFIELDS,data)
        self.fetch()
        self.process()
        return self

    def saveimage(self,url,path,base='images/',ref=''):
        image = pycurl.Curl()
        buffer = StringIO()
        image.setopt(image.URL, url)
        image.setopt(image.WRITEDATA, buffer)
        image.setopt(image.REFERER,ref)
        image.setopt(image.HTTPHEADER, ['User-Agent: Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',\
                                  'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
                                  'Accept-Language: en-US,en;q=0.5',\
                                  'Connection: keep-alive'])
        image.perform()
        image.close()
        data = buffer.getvalue()
        if path[-1] != '/':
            path = path + '/'
        path = path.replace("http://","")
        path = base+path
        pathSplit = path.split("/")
        nextPath='./'
        for i in pathSplit:
            nextPath = os.path.join(nextPath, i)
            try:
                os.mkdir(nextPath)
            except:
                pass
        filePath = nextPath+url.rsplit('/',1)[-1]
        file = open(filePath,'w')
        file.write(data)
        file.close()

    def get(self):
        self.fetch()
        self.process()
        return self

    def fetch(self):
        self.buffer.truncate(0)
        self.curl.perform()
        #self.curl.close()
        return self

    def fromstring(self,string,url):
        self.data = string
        self.doc=lh.document_fromstring(self.data)
        self.url = url
        return self

    def process(self):
        self.data = self.buffer.getvalue()
        self.doc=lh.document_fromstring(self.data)
        return self

    def save(self,path):
        file = open(path, 'w')
        try:
            file.write(self.data)
        except:
            try:
                file.write(self.data.encode('utf8','ignore'))
            except:
                file.write(self.data.encode('ascii','ignore'))
        file.close()
        file = open(path+'.url','w')
        file.write(self._url)
        file.close()

    def load(self,path):
        file = open(path+'.url','r')
        url = file.read()
        file.close()
        file = open(path, "r")
        self.fromstring(file.read(),url)
        file.close()

