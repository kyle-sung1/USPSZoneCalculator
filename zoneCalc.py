"""
Script that will calculate zone and shipping price based on:
a CSV containing recipient zip codes,
user input for the zone of origination,
and user input for parcel weight,
for First Class Commercial parcels. Output is CSV that contains:
zip code, shipping zone, commerical rate
for each row in the CSV.
"""

import csv
import requests
from bs4 import BeautifulSoup


def calculate(fromZip, toZip, weight):
    """Creates a Response object from USPS shippingAPI, creates Soup object to parse HTML from text
    attribute of Response object, and returns Zone and Commercial Rates
    as strings in a list
    """
    url = ('https://secure.shippingapis.com/ShippingAPI.dll?' +
    'API=RateV4' +
    '&XML=<RateV4Request USERID="751JOSHU0578">' +
    '<Revision>2</Revision>' +
    '<Package ID="1ST">' +
    '<Service>First Class Commercial</Service>' +
    '<FirstClassMailType>Parcel</FirstClassMailType>' +
    '<ZipOrigination>' +
    fromZip +
    '</ZipOrigination>' +
    '<ZipDestination>' +
    toZip +
    '</ZipDestination>' +
    '<Pounds>0</Pounds>' +
    '<Ounces>' +
    weight +
    '</Ounces>' +
    '<Container>Rectangular</Container>' +
    '<Size>Variable</Size>' +
    '<Machinable>true</Machinable>' +
    '</Package></RateV4Request>')

    zonePriceList = list()
    r = requests.get(url) #intializes Response object
    soup = str(BeautifulSoup(r.text, 'html.parser')) #intializes Soup object

    rateIndex = soup.index('<commercialrate>')
    slicedSoup = soup[rateIndex:] #slices everything before priceIndex in Soup

    if '<zone>' in soup:
        #retrieving indicies
        zoneIndex = soup.index('<zone>')
        priceIndex = slicedSoup.index('<commercialrate>')
        dotIndex = slicedSoup.index('.')


        zonePriceList.append(soup[zoneIndex+6]) #append Zone
        if slicedSoup[priceIndex+17] == '.': #append Price
            zonePriceList.append(slicedSoup[priceIndex+16] +
            slicedSoup[dotIndex] + slicedSoup[dotIndex+1] + slicedSoup[dotIndex+2])

        elif slicedSoup[priceIndex+17] != '.': #guard against inflation when prices > $10
            zonePriceList.append(slicedSoup[priceIndex+16]+ slicedSoup[priceIndex+17] +
            slicedSoup[dotIndex] + slicedSoup[dotIndex+1] + slicedSoup[dotIndex+2])

        return zonePriceList
    else:
        return " No zone or price found"


#------------------------------CSV opener----------------------#
# intialize empty lists
codeList = list() #nested list with zip codes in each list that is nested
calcList = list() #nested list with zip codes and corresponding Zones
origination = input("Zip code of origination: ")
weight = input("Parcel weight in ounces: ")

if int(weight) > 13:
    raise ValueError("Entered weight exceeds First Class mail requirements (13oz)")

with open('zipCode.csv') as fin: #open csv
    f = csv.reader(fin)
    for code in f:
        if len(code[0]) < 5: #adds 0's to zip codes with less than 5 numbers
            code.append('0'*(5-len(code[0])) + code[0])
            print("{} had only {} characters, added {} 0's".format(code[0], len(code[0]), (5-len(code[0]))))
            code.remove(code[0])
            codeList.append(code)
        elif len(code[0]) == 5:
            codeList.append(code) #appends zipCodes in list form

    for zipCode in codeList: #calculate zone for every zip
        zipCode.extend(calculate(origination, zipCode[0], weight))
        calcList.append(zipCode)

with open('zip-zones.csv', 'w') as fin: #write in new csv
    writeFile = csv.writer(fin)
    writeFile.writerows(calcList)






if __name__ == '__main__':
    #calculate('07054', '01267')
    pass
