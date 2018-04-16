def test():
    # lxml testing
    page = io.StringIO("<html><head><meta name='Hello' content='World'></meta></head><body><p>Body</p></body></html>")

    # x = lxml.etree.HTML(page)
    # x.xpath('<head></head>')

    tree = lxml.etree.parse(page)
    # /head/meta
    # /head/meta - absolute way
    # head/meta - relative way
    node = tree.xpath('//meta')  # xPath method process with xPath language
    print("An amount of node:", len(node))
    if (0 != len(node)):
        print(node[0].tag)
    else:
        print("Node is None")

    root = tree.getroot()
    print(root[0].tag)

    expr = "//*[local-name() = $name]"
    print(root.xpath(expr, name="html")[0].tag)

    print('Done')

    # Requests testing
    # url = 'https://habrahabr.ru'
    # r = requests.get(url)
    # print(r.text)
    # with open('test.html', 'w') as output_file:
    #     text = r.text # .encode(encoding='UTF-8',errors='strict')
    #     output_file.write(text) # cp1251