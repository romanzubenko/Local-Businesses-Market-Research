from pyquery import PyQuery as pq
from lxml import etree
import os,re,glob,urllib,urlparse,json,time 

class getterEmails(object):
    #Class Variables
    websites = []
    emails = {}
    country = ""

    def getLinks(self, j, url):
        domain = self.getDomain(url)
        links = []
        rawLinks = j("a")
        if len(rawLinks) != 0:
            
            for rawLink in rawLinks:
                href = j(rawLink).attr("href")
                #href = unicode(href, errors='ignore')
                if self.getDomain(href) == domain:
                    links.append(href)
        else:
            return []

        #print "links : " + str(links)
        return links

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

        


    def getEmailList(self,document):
        emails = []
        emails = re.findall('([A-Za-z0-9._+]+@+[A-Za-z0-9]+\.[-.A-Za-z]{2,6})',document)
        return emails    

    def processPage(self,unvisitedPages,visitedPages,emails):
        url = unvisitedPages[len(unvisitedPages) - 1]
        url = self.iriToUri(url)
        visitedPages.append(url)
        del unvisitedPages[len(unvisitedPages) - 1]
        newEmails = []

        try:
            document = urllib.urlopen(url)
            document = document.read()
            j = pq(document)
            newEmails = self.getEmailList(document)
        
        
            temporaryLinks = set(self.getLinks(j,url)).difference(set(unvisitedPages))
            temporaryLinks = temporaryLinks.difference(set(visitedPages))
            temporaryLinks = list(temporaryLinks)
            
            for link in temporaryLinks:
                unvisitedPages.append(link)

        except Exception as e:
            #inform them that a general error has occurred 
            print "error"

        
        
        for email in newEmails:
            emails.append(email)



    def processWebsite(self, url,ind):
        url = url.split("%2F")[0]
        print str(ind) +" website : "+ url
        self.emails[url] = []
        startTime = time.time()

        unvisitedPages = []
        visitedPages = []
        emails = []
        unvisitedPages.append(url)

        while len(unvisitedPages) != 0:
            if len(visitedPages) > 50:
                break

            if time.time() - startTime > 60:
                break

            self.processPage(unvisitedPages,visitedPages,emails)

        print str(emails) + "\n\n"
        self.emails[url] = emails
        

       
    def loopOverWebsites(self):
        url = ""
        j = 0
        for i in range (0,len(self.websites)):
            self.processWebsite(self.websites[i],i)
            if (i % 4 == 0):
                self.safeSave()


    def outputFile(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/"+self.country  # insert the path to the directory of interest
        dirList = os.chdir(path)
        f = open(self.country+"_emails.txt",'w')
        output = json.dumps(self.emails)

        f.write(output)
        f.close()
        return

    def safeSave(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/"+self.country  # insert the path to the directory of interest
        dirList = os.chdir(path)
        f = open(self.country+"_emails_safe.txt",'w')
        output = json.dumps(self.emails)

        f.write(output)
        f.close()
        return

    def unique(self,seq):
        set1 = set(seq)
        return list(set1)

    def urlEncodeNonAscii(self,b):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(self,iri):
        parts = urlparse.urlparse(iri)
        return urlparse.urlunparse(
            part.encode('idna') if parti==1 else self.urlEncodeNonAscii(part.encode('utf-8'))
            for parti, part in enumerate(parts)
    )

    def buildWebsites(self):
        path = "/Users/Roman/Documents/workspace/marketResearchPython/"+self.country  # insert the path to the directory of interest
        dirList = os.chdir(path)
        temp = []
        f = open(self.country+"_websites.txt", 'r')
        self.websites = json.loads(f.read())
        #self.websites = self.unique(self.websites)
        print self.country +": total websites to lurk : " + str (len(self.websites))

    def __init__(self, country):
        self.country = country
        self.buildWebsites()
        self.loopOverWebsites()
        self.outputFile()

        return

country = "Australia"
test = getterEmails(country)
