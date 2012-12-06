
import urllib,json,os,glob,re,urlparse,time
from pyquery import PyQuery as pq
from lxml import etree
from datetime import date

class Research(object):
    #Class Variables
    search = ""
    cities = []
    fileName = ""
    numberOfBiz = 0

    db = [] #main database with dictionaries [ name,town,yelp,url,[emails] ]

    '''
    db entry : {
        name : "",
        yelpPage : "",
        website : "",
        phone : "",
        address : "",
        email : "",
        town: "",
        state: "",
        country: ""
    }
    '''
    
    # START SEARCH SECTION, FETCHES YELP PAGES
    def getYelpPages(self):
        for place in self.places:
            self.processSearch(place)
        
    # fetches yelp pages for single place
    def processSearch(self,place):
        placeQuery = place['town']
        if place['state'] != "":
            placeQuery += ",+"+place['state']
        if place['country'] != "":
            placeQuery += ",+"+place['country']

        query = "http://www.yelp.com/search/snippet?&find_desc="+self.search+"&find_loc="+placeQuery+"&request_origin=user&rpp=40&show_filters=1&sortby=best_match"

        startIndex = 0

        while True:
            try:
                page = urllib.urlopen(query+"&start="+str(startIndex))
                page = page.read()
                page = json.loads(page)
                length = len(page['events']['search.map.overlays'])
            except Exception as e:
                return
    
            if length == 0:
                break

            self.processSearchPage(page,place,length)
            startIndex += length
            print "index = " + str(startIndex)
        return


    def processSearchPage(self,page,place,length):
        for i in range (0,length):
            entry = {'name' : "",'yelpPage' : "",'website' : "",'phone' : "",'adress' : "",'email' : "",'town': "",'state': "",'country': ""}
            
            entry['name'] = page['events']['search.map.overlays'][i]['encodedHTML'].split("<h3>")[1].split("</h3>")[0],
            entry['yelpPage'] = "http://www.yelp.com"+page['events']['search.map.overlays'][i]['url']
            entry['town'] = place['town'] 
            entry['state'] = place['state'] 
            entry['country'] = place['country'] 


            self.db.append(entry)
        return

    # END OF SEARCH SECTION, FETCHES YELP PAGES
    # 


    def getInfo(self):
        if self.params['website'] == 0 and self.params['phone'] == 0 and self.params['address'] == 0 and self.params['email'] == 0:
            return

        print "getting info..."
        for entry in self.db:
            self.processBusinesspage(entry)

        return

    def processBusinesspage(self,entry):

        try:
            print entry['yelpPage']
            j = pq(url=entry['yelpPage'])
        except Exception as e:
            print "fail"
            return

        if self.params['website'] == 1:
            entry['website'] = self.getWebsite(j)

        if self.params['phone'] == 1:
            entry['phone'] = self.getPhone(j)
        if self.params['address'] == 1:
            entry['address'] = self.getAddress(j)
        if self.params['email'] == 1:
            entry['email'] = self.getEmails(j)



    def getAddress(self,j):
        address = ""
        pointer = j('address').children()

        for line in pointer:
            address += " "+str(j(line).html())
        return address

    def getPhone(self,j):
        print "phone "+str(j("#bizPhone").html())
        return j("#bizPhone").html()

    def getWebsite(self, j):
        url = j("#bizUrl")
        if len(url) != 0:
            url = j(url.children()[0]).attr("href")
            url = url.split("biz_redir?url=http%3A%2F%2F")
            
            if (len(url) > 1):
                url = url[1]
            else:
                url = url[0]
                
                url = url.split("biz_redir?url=https%3A%2F%2F")
                if (len(url) > 1):
                    url = url[1]
                else:
                    url = url[0]
            

            url = url.split("&src_bizid")
            url = url[0]

            url = url.split("%2F")
            url = url[0]

            url = "http://"+url
            print url
        else:
            return ""

        return url
        

    def getEmails(self):
        return []

    def getEmailList(self,document):
        emails = []
        emails = re.findall('([A-Za-z0-9._+]+@+[A-Za-z0-9]+\.[-.A-Za-z]{2,6})',document)
        return emails  
                

    def getDomain(self,url):
        tempUrl = " " + url;
        if len(tempUrl.split("www.")) > 1:
            url = tempUrl.split("www.")[1].split("/")[0]
        elif len(tempUrl.split("http://")) > 1:
            url = tempUrl.split("http://")[1].split("/")[0]
        elif len(tempUrl.split("https://")) > 1:
            url = tempUrl.split("https://")[1].split("/")[0]
        
        url = url.split("/")[0]
        url = url.split("%2F")[0]

        return url




    def writeDatabase(self):
        f = open(self.search +"_"+date.isoformat(date.today())+".txt",'w')
        output = json.dumps(self.db)

        f.write(output)
        f.close()
        return


    #constructor
    '''
    params = {
        website: 0,
        phone: 0,
        address: 0,
        email : 0
    }

    places = [] of place

    place = {
        town: "",
        state: "",
        country: ""
    }

    '''
    def __init__(self, searchQuery,places,params):
        self.search = searchQuery
        self.places = places
        self.params = params
        
        self.getYelpPages()
        self.getInfo()
        self.writeDatabase()

        return


#cities = ["London","Birmingham","Manchester","Liverpool","Newcastle","Nottingham","Sheffield","Leeds","Bristol","Middlesbrough","Leicester","Portsmouth","Bradford","Bournemouth","Reading","Huddersfield","Stoke","Coventry","Birkenhead","Southampton","Hull","Sunderland","Wigan","Brighton","Southend","Preston","Blackpool","Bolton","Aldershot","Plymouth","Luton","Chatham","Derby","Barnsley","Northampton","Norwich","Milton+Keynes","Worthing","Crawley","Rochdale","Warrington","Mansfield","Swindon","Burnley","Ipswich","Oxford","Wakefield","Grimsby","York","Telford","Doncaster","Peterborough","Gloucester","Blackburn","Cambridge","Hastings"]
#cities = ["Sydney","Melbourne","Brisbane","Perth","Adelaide"," Gold+Coast","Newcastle","Canberra","Queanbeyan","Wollongong","Sunshine+Coast","Greater+Hobart","Geelong","Townsville","Cairns","Darwin","Toowoomba","Launceston","Albury-Wodonga","Ballarat","Bendigo","Mandurah","Burnie-DevonportMackay"]
places = [{'town': "Boston",'state': "MA",'country': "USA"}]
params = {
        'website': 1,
        'phone': 1,
        'address': 1,
        'email' : 0
    }

r = Research("photo+studio",places,params)





