__author__ = 'walter'

import requests
from xml.etree import ElementTree as ET


OCS_ADMIN = 'ocs/v1.php/cloud'

class StatusCodeException(Exception):
    def __init__(self,status,statusCode,message):
        self.status = status
        self.statusCode = statusCode
        self.message = message
    def __str__(self):
        errMsg = self.status
        if self.message != '':
          errMsg = ':'+self.status
        return repr(errMsg)

class Response(object):

    def __init__(self,textResponse):
        #init parse
        self.__resxml = ET.fromstring(textResponse)
        self.__meta = self.__resxml.find('meta')
        self.__status = self.__meta.find('status').text
        self.__statuscode = self.__meta.find('statuscode').text
        if self.__meta.find('message') is not None:
            self.__message = self.__meta.find('message').text
    @property
    def status(self):
        return self.__status

    @property
    def statuscode(self):
        return int(self.__statuscode)

    @property
    def message(self):
        return getattr(self,'__message','')

    def getElementData(self):
        data = self.__resxml.find('data')
        return data

    def getData(self):
        pass

class Client(object):

    def __init__(self,url,username, password,**kwargs):

        if not url[-1] == '/':
            url = url + '/'

        self.url = url + OCS_ADMIN
        self.__auth = (username,password)
        self.__debug = kwargs.get('debug', False)

    def __cast(self,tag):
        if tag in ['displayname','email','quota']:
            return str
        elif tag in ['']:
            return int
        elif tag in ['']:
            return float
        elif tag in ['enabled']:
            return bool

    def __compileUrl(self,apiName,*args,**kwargs):
        url = self.url + '/' + apiName
        if len(args) > 0:
            url += '/' + '/'.join(args)
        return url


    def __makeRequest(self,apiName,*args,**kwargs):
        r = requests.get(self.__compileUrl(apiName,*args,**kwargs),auth=self.__auth)
        r.raise_for_status()
        res = Response(r.text)
        if res.statuscode != 100:
            raise StatusCodeException(res.status,res.statuscode,res.message)
        return res

    def getUsers(self):
        toRet = []
        res = self.__makeRequest('users')
        data = res.getElementData()
        for u in list(data.find('users')):
            toRet.append(u.text)
        return toRet

    def getUser(self,userName):
        toRet = {}
        res = self.__makeRequest('users',userName)
        data = res.getElementData()
        for u in list(data):
            toRet[u.tag] = self.__cast(u.tag)(u.text)
        return toRet
