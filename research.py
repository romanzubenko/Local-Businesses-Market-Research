
import urllib,json,os,glob,re,urlparse
from pyquery import PyQuery as pq
from lxml import etree

import getYelpPages as yp



class Research(object):
    #Class Variables
    search = ""
    cities = []
    fileName = ""
    numberOfBiz = 0

    database = [] #main database with dictionaries [ name,town,yelp,url,[emails] ]
    bizNames = []
    bizYelpPages = []
    bizUrls = []
    bizEmails = []
    
    def addToDatabaseDictionary(self):
        return

    def getYelpPages(self):
        length = len(self.cities)
        for city in range (0,length):
            print "city = " + self.cities[city]
            getter = yp.GetterYelpPages("http://www.yelp.com/search/snippet?&find_desc=recording+%26+rehearsal+studios&find_loc="+self.cities[city]+",+Australia&request_origin=user&rpp=40&show_filters=1&sortby=best_match",self.cities[city]+".txt")
        self.bizYelpPages = getterYelpPages.get()

    def getWebsites(self):
        getter = getterYelpPages()
        self.bizUrls = getterWebsites.get()

    def getEmails(self):
        getter = getterEmails(self.bizUrls)
        self.bizEmails = getterEmails.get()

    def writeDatabase(self):
        return


    #constructor
    def __init__(self, search,cities,fileName):
        self.search = search
        self.cities = cities
        self.fileName = fileName
        
        self.getYelpPages()
        #self.getWebsites()
        #self.getEmails()
        #self.writeDatabase()

        return







#cities = ["London","Birmingham","Manchester","Liverpool","Newcastle","Nottingham","Sheffield","Leeds","Bristol","Middlesbrough","Leicester","Portsmouth","Bradford","Bournemouth","Reading","Huddersfield","Stoke","Coventry","Birkenhead","Southampton","Hull","Sunderland","Wigan","Brighton","Southend","Preston","Blackpool","Bolton","Aldershot","Plymouth","Luton","Chatham","Derby","Barnsley","Northampton","Norwich","Milton+Keynes","Worthing","Crawley","Rochdale","Warrington","Mansfield","Swindon","Burnley","Ipswich","Oxford","Wakefield","Grimsby","York","Telford","Doncaster","Peterborough","Gloucester","Blackburn","Cambridge","Hastings"]
cities = ["Sydney","Melbourne","Brisbane","Perth","Adelaide"," Gold+Coast","Newcastle","Canberra","Queanbeyan","Wollongong","Sunshine+Coast","Greater+Hobart","Geelong","Townsville","Cairns","Darwin","Toowoomba","Launceston","Albury-Wodonga","Ballarat","Bendigo","Mandurah","Burnie-DevonportMackay"]
r = Research("",cities,"UK")

