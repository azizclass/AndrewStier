__author__ = 'Andrew'

import json
import sys
import re
import urllib
import cgi

from bs4 import BeautifulSoup

def unicodeToHTMLEntities(text):
    text = cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    return text

def contractAsJson(filename):

    #Specifically, you need to return a JSON object with 3 fields.
    #  first is the current price of the stock;
    #  the second is the URLs corresponding to the other expiration days;
    #  the third is a list of the detailed individual contracts sorted in decreasing order of open interest.

    data = open(filename, 'r')

    soup = BeautifulSoup(data, 'html.parser')
    #print(soup.prettify())
    #print soup.get_text()

    # for string in soup.stripped_strings:
    #     print(repr(string))

    pricetag =  soup.find(id = re.compile("^yfs_l84_"))
    priceS = pricetag.get_text()
    price = float(priceS)
    #print price

    all_links = soup.find_all(href = re.compile("m="))
    #links = all_links.find_all(href = re.compile("/q/op?s="))

    date_url = []
    for link in all_links:
        # print link
        # print link.get('href')
        # print unicodeToHTMLEntities(link.get('href'))
        href = str(link.get('href'))


        if href.startswith("/q/o"):
            #print link.get('href')
            #print "http://finance.yahoo.com" + link.get('href')
            date_url.append("http://finance.yahoo.com" + unicodeToHTMLEntities(link.get('href')))


    #print date_url

    # for url in date_url:
    #     print url
    DictList = []

    def has_nowrap(tag):
        return tag.has_attr('nowrap')


    tables = soup.findAll(class_ = "yfnc_datamodoutline1")
    for table in tables:
        #print table
        rows = table.findAll(has_nowrap)
        for row in rows:
            D = {}
            strike = row
            strikev = strike.string
            D["Strike"] = strikev

            #Move to the symbol/date/type entry
            s = strike.next_sibling
            s1 = s.string

            #Find the first numerical number and store the symbol
            m1 = re.search("\d", s1)
            #print s1
            index1 = m1.start()
            #print s1[index1]
            if s1[index1]== "7":
                #print "yes"
                index1 = index1 + 1
            symbolv = s1[:index1]
            D["Symbol"] = symbolv

            #Get a string that excludes the symbol
            s2 = s1[index1:]

            #Find the index of the first letter and store it as index2
            index2 = 0
            for character in s2:
                if character.isdigit():
                    index2 = index2+1
                else:
                    break

            #Store the date and the type in the dictionary
            D['Date'] = s2[:index2]
            #print s2[:index2]
            D['Type'] = s2[index2]
            #print s2[index2]

            #Move to the "last" entry
            last = s.next_sibling
            #print last
            lastv = last.string
            D['Last'] = lastv

            #Move to the change entry
            change = last.next_sibling
            change_tag = change.b
            #print change_tag.string
            changev = " " + change_tag.string
            D['Change'] = changev

            #Move to the bid entry
            bid = change.next_sibling
            bidv = bid.string
            D['Bid'] = bidv

            #Move to the ask entry
            ask = bid.next_sibling
            askv = ask.string
            D['Ask'] = askv

            #Move to the vol entry
            vol = ask.next_sibling
            D['Vol'] = vol.string

            #Move to the open entry
            op = vol.next_sibling
            D['Open'] = op.string


            #print D

            DictList.append(D)




    def openint(x):
        open1 = x['Open']
        openx = ""
        for char in open1:
            if char.isdigit():
                openx = openx + char

        return int(openx)

    DictList.sort(lambda x,y: openint(y) - openint(x))

    # for dict in DictList:
    #     print dict



    jsonDict = {}
    jsonDict['currPrice'] = price
    jsonDict['dateUrls'] = date_url
    jsonDict['optionQuotes'] = DictList

    data =  { 'currPrice':price, 'dateUrls':date_url, 'optionQuotes':DictList }


    jsonQuoteData = json.dumps(data)

    #print 'JSON:', jsonQuoteData

    return jsonQuoteData