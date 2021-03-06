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
    #updates skuList
    #malformed CSV data presents a potential security risk
    global skuList
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        for row in csv.reader(csvfile):
            skuList.append(row[0])
        csvfile.close()
    #print("skuList contents inside of READCSV: ",skuList)
    return skuList
#================================
#BEGIN SEARCH family
def singleSkuSearchMetaData(sku):
    global loggedUser, loggedPass
    url = "https://s7sps1apissl.scene7.com/scene7/services/IpsApiService"
    print("searching s7 for: [{}] family".format(sku))
    payload_header="<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\">\r\n <soap:Header>\r\n <ns:authHeader>\r\n <!--Optional:-->\r\n <ns:user>{}</ns:user>\r\n <!--Optional:-->\r\n <ns:password>{}</ns:password>\r\n <ns:appName>bertz</ns:appName>\r\n <ns:appVersion>7</ns:appVersion>\r\n </ns:authHeader>\r\n </soap:Header>\r\n <soap:Body>\r\n <ns:getAssetsByNameParam>\r\n<ns:companyHandle>c|8676</ns:companyHandle>\r\n <ns:nameArray>\r\n".format(loggedUser,loggedPass)
    payload_main ="<ns:items>{}</ns:items>\r\n".format(sku)
    payload_alts = ""
    for alt in range(1,16):
        payload_alts+="<ns:items>{}_alt{}</ns:items>\r\n".format(sku,alt)

    #payload_body = "</ns:nameArray>\r\n<ns:responseFieldArray>\r\n<ns:items>assetArray/items/name</ns:items>\r\n<ns:items>assetArray/items/lastModified</ns:items>\r\n<ns:items>assetArray/items/lastModifUser</ns:items>\r\n</ns:responseFieldArray>\r\n</ns:getAssetsByNameParam>\r\n </soap:Body>\r\n</soap:Envelope>"

    payload_body = '''\
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

    #print("This is payload\r\n"+payload)
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.content
#================== end singleSkuSearchMetaData===========

def searchSkuMetaData(searchList):
    _privateMetaList = []
    if len(searchList)>0:
        for _sku in searchList:
            for entry in parseMetaDataResponse(singleSkuSearchMetaData(_sku)):
                _privateMetaList.append(entry) #add each entry inside of the parseMetaDataResponse function into the private list
            #end for entry loop
        #end _sku iteration
    else:
        return False
    return _privateMetaList
#================== end searchSkuMetaData function=========




#================== begin parseMetaDataResponse=============
def parseMetaDataResponse(responseXML):
    #returns a reference to a list
    #print("parseMetaDataResponse function called")
    # TEST for no items found!
    root = etree.XML(responseXML, etree.XMLParser(remove_blank_text=True))
    #print(etree.dump(root))
    assetArray = root[0][0][0]
    _skuMetaData = []
    xmlNS = "{"+etree.QName(root[0][0]).namespace+"}"
    for item in assetArray.iter(xmlNS+"items"):
        for child in item.iter():
            if etree.QName(child).localname == "assetHandle":assetHandle=child.text
            if etree.QName(child).localname == "type":assetType=child.text
            if etree.QName(child).localname == "name":assetName=child.text
            if etree.QName(child).localname == "lastModified":lastModified=child.text
            if etree.QName(child).localname == "lastModifyUser":lastModifyUser=child.text
            if etree.QName(child).localname == "width":assetWidth=child.text
            if etree.QName(child).localname == "height":assetHeight=child.text
            if etree.QName(child).localname == "fileSize":assetFileSize=child.text
        _skuMetaData.append([assetHandle,assetType,assetName,assetWidth,assetHeight,assetFileSize,lastModified,lastModifyUser])
    print("Metadata Parsed for family, proceed.")
    return _skuMetaData
#================= end parseMetaDataResponse





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

csv_path = input("Please enter CSV Path (including filename)")
print(*searchSkuMetaData(readCSV(csv_path)),sep="\n")
print("this is skuList",skuList)
