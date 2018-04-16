import sys
import io
# lxml
import lxml
from lxml import etree
# xml parser
import xml.etree.cElementTree as et
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
# custom libs
import crawler

# class Usage():
#     def __init__(self, msg):
#        self.msg = msg

def get_smth_from_html_data(data):
    parser = etree.HTMLParser()
    page = io.StringIO(data)
    tree = lxml.etree.parse(page, parser)
    imgNodes = tree.xpath('//img[@src and string-length(@src)!=0]')
    imageList = []
    for node in imgNodes:
        imageList = imageList + [node.attrib['src']]
    textNodes = tree.xpath('//p[string-length(text()) > 0]')
    textList = []
    for node in textNodes:
        text = node.text
        if text != None:
            textList = textList + [text]
    return imageList, textList


def get_smth_from_xml_data(data):
    parser = etree.XMLParser()
    page = io.StringIO(data)
    tree = lxml.etree.parse(page, parser)
    root = tree.getroot()
    pageNodesCount = len(root.getchildren())
    print("Pages count: %s" % pageNodesCount)
    pagesDict = {}
    for pageNode in range(1, pageNodesCount+1):
        xPathCountFragmentsStr = "count(/data/page[position() = %s]/fragment[@type = 'text'])" % pageNode
        fragmentsTextNodesCount = tree.xpath(xPathCountFragmentsStr)
        xPathGetPageUrlStr = "/data/page[position() = %s]" % pageNode
        pageNodeUrl = tree.xpath(xPathGetPageUrlStr)
        url = pageNodeUrl[0].attrib['url']
        print("%s has text fragments count: %s" % (url, fragmentsTextNodesCount))
        pagesDict.update({url: fragmentsTextNodesCount})
    maxCount = -1
    for url, count in pagesDict.items():
        if count > maxCount:
            maxCount = count
    isMaxFound = 0
    for url, count in pagesDict.items():
        if count == maxCount:
            print("%s has maximal text fragments count: %s" % (url, count))
            isMaxFound = 1
    if not isMaxFound:
        print("Maximum's not existing")


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'windows-1251') # utf-8
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='windows-1251') # UTF-8 / windows-1251


def create_xml_template(urlPlusTextAndImgStrs):
    top = Element('data')
    for url, data in urlPlusTextAndImgStrs.items():
        pages = SubElement(top, 'page')
        pages.set('url', url)
        for type, list in data.items():
            for str in list:
                element = SubElement(pages, 'fragment')
                element.text = str
                element.set('type', type)
    return prettify(top)


def do_web_crawling_and_create_xml_results_data(urlToCrawling, maxAmountOfPagesToCrawling):
    fileNameToWrite = 'data.xml'
    # https://rozetka.com.ua/
    urlPlusDataDict = crawler.spider(urlToCrawling, maxAmountOfPagesToCrawling)
    urlPlusTextAndImgStrs = {}
    for url, data in urlPlusDataDict.items():
        imagesList, textList = get_smth_from_html_data(data)
        urlPlusTextAndImgStrs.update({url: {'text': textList, 'image': imagesList}})
    data = create_xml_template(urlPlusTextAndImgStrs)
    with open(fileNameToWrite, 'wb') as output_file:
        output_file.write(data)
    return fileNameToWrite


def do_xml_parsing_and_counting_text_fragments(fileName):
    with open(fileName, 'r') as input_file:
        dataList = input_file.readlines()
        dataList.pop(0)
        get_smth_from_xml_data(''.join(dataList))


# main function
def main(argv=None):
    if argv is None:
        argv = sys.argv
    # Task 1
    fileName = do_web_crawling_and_create_xml_results_data("http://kpi.ua/", 5)
    # Task 2
    do_xml_parsing_and_counting_text_fragments('data.xml')
    print("Program's completed")


# main calling
if __name__ == "__main__":
    sys.exit(main())

