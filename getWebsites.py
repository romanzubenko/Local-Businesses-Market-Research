
import urllib
from pyquery import PyQuery as pq
from lxml import etree
import os
import json
import glob


class getterWebsites(object):
    #Class Variables
    websites = []
    yelpPages = []

    def get(self):
        return websites
        
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

    def outputFile(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/Australia"  # insert the path to the directory of interest
        dirList = os.chdir(path)
        f = open("Aus_websites.txt",'w')
        output = json.dumps(self.websites)
        f.write(output)
        f.close()
        return

       
    def loopOverPages(self):
        url = ""
        j = 0
        for i in range (0,len(self.yelpPages)):
            try:
                d = pq(url="http://www.yelp.com"+self.yelpPages[i])
                url = self.getWebsite(d)

                if url != "":
                    j += 1
                    print "url " + str(j) +" out of "+str(i)
                    self.websites.append(url)
            except Exception as e:
                #inform them that a general error has occurred 
                print "ERROR " + str(j) +" out of "+str(i)

    def unique(self,seq):
        # Not order preserving    
        set1 = set(seq)
        return list(set1)

    def buildYelpPages(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/Australia/cities"  # insert the path to the directory of interest
        dirList = os.chdir(path)
        temp = []
        for fname in glob.glob("*.txt"):
            f = open(fname, 'r')
            temp = json.loads(f.read())
            self.yelpPages = self.yelpPages + temp


        print len(self.yelpPages)
        self.yelpPages = self.unique(self.yelpPages)
        print len(self.yelpPages)

    def __init__(self):
        self.buildYelpPages()
        self.loopOverPages()
        self.outputFile()

        print self.websites
        

r = getterWebsites()
