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
    imagesStr = ''
    for node in imgNodes:
        # print(node.attrib['src'])
        imagesStr += (node.attrib['src'] + '\n')
    textNodes = tree.xpath('//p[string-length(text()) > 0]')
    textStr = ''
    for node in textNodes:
        text = node.text
        if text != None:
            textStr += (text + ';; ')
        # if text != None:
        #     for symbol in text:
        #         if symbol != ' ':
        #             textStr += (text + '\n')
        #             break
    return imagesStr, textStr


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'windows-1251') # utf-8
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='windows-1251') # UTF-8 / windows-1251


def create_xml_template(urlPlusTextAndImgStrs):
    top = Element('data')
    for url, data in urlPlusTextAndImgStrs.items():
        pages = SubElement(top, 'page')
        pages.set('url', url)
        for type, str in data.items():
            element = SubElement(pages, 'fragment')
            element.text = str
            element.set('type', type)
    return prettify(top)


def do_web_crawling_and_create_xml_results_data(urlToCrawling, maxAmountOfPagesToCrawling):
    # http://lxml.de/FAQ.html - ideal example
    # http://kpi.ua/
    # https://rozetka.com.ua/
    urlPlusDataDict = crawler.spider(urlToCrawling, maxAmountOfPagesToCrawling)
    urlPlusTextAndImgStrs = {}
    for url, data in urlPlusDataDict.items():
        imagesStr, textStr = get_smth_from_html_data(data)
        urlPlusTextAndImgStrs.update({url: {'text': textStr, 'image': imagesStr}})
    data = create_xml_template(urlPlusTextAndImgStrs)
    # print(data)
    with open('data.xml', 'wb') as output_file:
        output_file.write(data)


# main function
def main(argv=None):
    if argv is None:
        argv = sys.argv
    do_web_crawling_and_create_xml_results_data("http://kpi.ua/", 5)
    print("Program's completed")


# main calling
if __name__ == "__main__":
    sys.exit(main())

