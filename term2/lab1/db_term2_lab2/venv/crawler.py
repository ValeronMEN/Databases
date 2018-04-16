from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import requests


class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a': # we are looking for links
            for (key, value) in attrs:
                if key == 'href':
                    # We combine a relative URL with the base URL to create
                    # an absolute URL
                    newUrl = parse.urljoin(self.baseUrl, value)
                    isLinkWithoutSharpOrEtc = 1
                    isLinkNotExistingInList = 1
                    for symbol in newUrl:
                        if symbol == '#' or symbol == '?':
                            isLinkWithoutSharpOrEtc = 0
                            break
                    if isLinkWithoutSharpOrEtc:
                        self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        # print(response.getheader('Content-Type'))
        contentTypeHeader = response.getheader('Content-Type')
        if contentTypeHeader=='text/html' or \
                contentTypeHeader=='text/html; charset=utf-8' or \
                contentTypeHeader=='text/html; charset=UTF-8' or \
                contentTypeHeader=='text/html;charset=UTF-8':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString) # string, not bytes
            return htmlString, self.links
        else:
            return "",[]


def spider(url, maxPages):
    pagesToVisit = [url]
    pagesWereVisited = []
    numberVisited = 0
    toReturn = {}
    while numberVisited < maxPages and pagesToVisit != []:
        numberVisited = numberVisited + 1
        url = pagesToVisit[0]
        pagesWereVisited = pagesWereVisited + [url]
        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            if (data == ""):
                print("Something's wrong")
            toReturn.update({url: data})
            for link in links:
                isLinkNotExistingInListToVisit = 1
                isLinkNotExistingInVisitedList = 1
                for linkToVisit in pagesToVisit:
                    if link == linkToVisit:
                        isLinkNotExistingInListToVisit = 0
                        break
                if isLinkNotExistingInListToVisit:
                    for linkWasVisited in pagesWereVisited:
                        if link == linkWasVisited:
                            isLinkNotExistingInVisitedList = 0
                            break
                if isLinkNotExistingInListToVisit and isLinkNotExistingInVisitedList:
                    pagesToVisit = pagesToVisit + [link]
            # print("Pages were visited: %s" % pagesWereVisited)
            with open('pagesToVisit.txt', 'w') as output_file:
                str = ''
                for link in pagesToVisit:
                    str += (link + '\n')
                output_file.write(str)
        except:
            print(" **Failed!**")
    print("Web crawling is completed")
    return toReturn