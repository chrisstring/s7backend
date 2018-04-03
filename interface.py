#!/usr/bin/env python3
#   interface.py
#   pip3 install lxml
#   sudo apt-get install python3-lxml
#
#   utilizes the SOAP1.2 bindings, we should see w3...2003/05 in the namespace
#   Interacts with scene7's backend to automate the process of finding assets, getting their size, ading them to a job queue
#   where the size < 1GB total and sending the jobs out for downloading.
#
#   XML content and exports from s7 need to be handled in the RAW not in the converted text. so response.content is the way to go
#   trueLogin is currently disabled



import requests, csv, os, getpass, xml.etree.ElementTree as ET
from lxml import etree
url = "https://s7sps1apissl.scene7.com/scene7/services/IpsApiService"

companyHandle = "c|8676"
masterU = "chris.string@turn5.com"
masterP = "Password2#"
loggedIn = False
sessionId = ""
skuList = []
loggedUser=""
loggedPass=""

#===========



#   authUser accepts username and password
def authUser(uname,pwd):
    global loggedUser,loggedPass
#    payload = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\">\r\n <soap:Header>\r\n <ns:authHeader>\r\n <!--Optional:-->\r\n <ns:user>{}</ns:user>\r\n <!--Optional:-->\r\n <ns:password>{}</ns:password>\r\n <ns:appName>bertz</ns:appName>\r\n <ns:appVersion>69</ns:appVersion>\r\n </ns:authHeader>\r\n </soap:Header>\r\n <soap:Body>\r\n <ns:checkLoginParam>\r\n <!--Optional:-->\r\n <ns:companyHandle>c|8676</ns:companyHandle>\r\n <ns:email>{}</ns:email>\r\n <ns:password>{}</ns:password>\r\n </ns:checkLoginParam>\r\n </soap:Body>\r\n</soap:Envelope>".format(masterU,masterP,uname,pwd)
#    headers = {'soapaction': "checkLogin",'cache-control': "no-cache"}

#    response = requests.request("POST", url, data=payload, headers=headers)

#   XML content and exports from scene7 payloads should be dealt with in the raw.

#    responseRoot = ET.fromstring(response.text)



    if uname=="chris.string@turn5.com" and pwd == "Password2#":
        loggedUser= uname
        loggedPass = pwd
        return True
    else:
        return False



#    if responseRoot[0][0][0].text.lower()=="success":
#        return True
#    else:
#        return False

# end authUser()



#   readCSV should accept a CSV file with multiple rows and one column, no headers
def readCSV(filename):
    with open('filename', 'r', newline='', encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            singleSkuSearch(row[0])

#================================
#BEGIN SEARCH family
def modifiedSkuSearch(sku):
    global loggedUser, loggedPass
    url = "https://s7sps1apissl.scene7.com/scene7/services/IpsApiService"
    print("searching s7 for: [{}] family".format(sku))
    payload_header="<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\">\r\n <soap:Header>\r\n <ns:authHeader>\r\n <!--Optional:-->\r\n <ns:user>{}</ns:user>\r\n <!--Optional:-->\r\n <ns:password>{}</ns:password>\r\n <ns:appName>bertz</ns:appName>\r\n <ns:appVersion>7</ns:appVersion>\r\n </ns:authHeader>\r\n </soap:Header>\r\n <soap:Body>\r\n <ns:getAssetsByNameParam>\r\n<ns:companyHandle>c|8676</ns:companyHandle>\r\n <ns:nameArray>\r\n".format(loggedUser,loggedPass)
    payload_main ="<ns:items>{}</ns:items>\r\n".format(sku)
    payload_alts = ""
    for alt in range(1,16):
        payload_alts+="<ns:items>{}_alt{}</ns:items>\r\n".format(sku,alt)

    #payload_body = "</ns:nameArray>\r\n<ns:responseFieldArray>\r\n<ns:items>assetArray/items/name</ns:items>\r\n<ns:items>assetArray/items/lastModified</ns:items>\r\n<ns:items>assetArray/items/lastModifUser</ns:items>\r\n</ns:responseFieldArray>\r\n</ns:getAssetsByNameParam>\r\n </soap:Body>\r\n</soap:Envelope>"

    payload_body = '''
    </ns:nameArray>
        <ns:responseFieldArray>
            <ns:items>assetArray/items/name</ns:items>
            <ns:items>assetArray/items/type</ns:items>
            <ns:items>assetArray/items/lastModified</ns:items>
            <ns:items>assetArray/items/lastModifyUser</ns:items>
            <ns:items>assetArray/items/assetHandle</ns:items>
            <ns:items>assetArray/items/imageInfo/fileSize</ns:items>
            <ns:items>assetArray/items/imageInfo/width</ns:items>
            <ns:items>assetArray/items/imageInfo/height</ns:items>
        </ns:responseFieldArray>
        </ns:getAssetsByNameParam>
    </soap:Body>
    </soap:Envelope>'''
    headers = {'soapaction': "getAssetsByName",'cache-control': "no-cache"}
    payload = payload_header+payload_main+payload_alts + payload_body

#    print("This is payload\r\n"+payload)
    response = requests.request("POST", url, data=payload, headers=headers)

    root = etree.XML(response.content)
    print(etree.tostring(root))


#   singleSkuSearch uses getAssetsByName
def singleSkuSearch(sku):
    global loggedUser, loggedPass
    url = "https://s7sps1apissl.scene7.com/scene7/services/IpsApiService"
    print("searching s7 for: [{}] family".format(sku))
    payload_header="<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\">\r\n <soap:Header>\r\n <ns:authHeader>\r\n <!--Optional:-->\r\n <ns:user>{}</ns:user>\r\n <!--Optional:-->\r\n <ns:password>{}</ns:password>\r\n <ns:appName>bertz</ns:appName>\r\n <ns:appVersion>7</ns:appVersion>\r\n </ns:authHeader>\r\n </soap:Header>\r\n <soap:Body>\r\n <ns:getAssetsByNameParam>\r\n<ns:companyHandle>c|8676</ns:companyHandle>\r\n <ns:nameArray>\r\n".format(loggedUser,loggedPass)
    payload_main ="<ns:items>{}</ns:items>\r\n".format(sku)
    payload_alts = ""
    for alt in range(1,16):
        payload_alts+="<ns:items>{}_alt{}</ns:items>\r\n".format(sku,alt)

    payload_body = "</ns:nameArray>\r\n </ns:getAssetsByNameParam>\r\n </soap:Body>\r\n</soap:Envelope>"
    headers = {'soapaction': "getAssetsByName",'cache-control': "no-cache"}
    payload = payload_header+payload_main+payload_alts + payload_body

#    print("This is payload\r\n"+payload)
    response = requests.request("POST", url, data=payload, headers=headers)

    responseRoot = ET.fromstring(response.text)
    print("This is response:\r\n"+response.text)

#======================= BEGIN TESTING HERE =============================

print("\t\t===Welcome to the Super Sweet Scene 7 Stuff Script (developer mode)===")
while loggedIn==False:
    print("Please provide your Scene 7 login credentials")
    inputUser = input("user email: ")
    inputPass = getpass.getpass("user password: ")

    if authUser(inputUser,inputPass):
        print("Credential check: PASS\nLogged In:")
        loggedIn=True
    else:
        print("Credential check: FAIL")


modifiedSkuSearch("T533729")
