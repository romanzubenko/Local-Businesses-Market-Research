
import urllib
import json
import os

class GetterYelpPages(object):
    #Class Variables
    searchUrl = ""
    bizYelpPages = [0]
    bizUrls = []
    searchPage = ""
    fileName = ""
    numberOfBiz = 0

    def processYelpPage(self,page,length,startIndex):
        globalIndex = startIndex
        for i in range (0,length):
            globalIndex += 1
            self.bizUrls.append(page['events']['search.map.overlays'][i]['url'])
            #print "biz =" +str(globalIndex) + ", url = "+ str(page['events']['search.map.overlays'][i]['url'])

        return

    def processSearch(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/cities"  # insert the path to the directory of interest
        dirList = os.chdir(path)
        startIndex = 0;
        f = open(self.fileName,'w')
      
        page = urllib.urlopen(self.search)
        page = page.read()
        page = json.loads(page)
        self.bizUrls = []

        length = len(page['events']['search.map.overlays'])

        while length > 0:
            self.processYelpPage(page,length,startIndex)

            startIndex += length
            page = urllib.urlopen(self.search+"&start="+str(startIndex))
            page = page.read()
            page = json.loads(page)
            length = len(page['events']['search.map.overlays'])


        print "number of businesses =" + str(startIndex)
        self.numberOfBiz += startIndex;
       

        output = json.dumps(self.bizUrls)
        f.write(output)
        f.close()

    def get(self):
        return self.bizUrls

    def __init__(self, search,fileName):
        self.search = search
        self.fileName = fileName
        self.processSearch()
        
'''
cities = ["London","Birmingham","Manchester","Liverpool","Newcastle","Nottingham","Sheffield","Leeds","Bristol","Middlesbrough","Leicester","Portsmouth","Bradford","Bournemouth","Reading","Huddersfield","Stoke","Coventry","Birkenhead","Southampton","Hull","Sunderland","Wigan","Brighton","Southend","Preston","Blackpool","Bolton","Aldershot","Plymouth","Luton","Chatham","Derby","Barnsley","Northampton","Norwich","Milton+Keynes","Worthing","Crawley","Rochdale","Warrington","Mansfield","Swindon","Burnley","Ipswich","Oxford","Wakefield","Grimsby","York","Telford","Doncaster","Peterborough","Gloucester","Blackburn","Cambridge","Hastings"]

for city in range (0,length):
            print "city = " + cities[city]
            getter = new GetterYelpPages("http://www.yelp.com/search/snippet?&find_desc=recording+%26+rehearsal+studios&find_loc="+cities[city]+"+UK&request_origin=user&rpp=40&show_filters=1&sortby=best_match",cities[city]+".txt")
'''
