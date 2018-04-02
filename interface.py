#!/usr/bin/env python3
#   interface.py
#   utilizes the SOAP1.2 bindings, we should see w3...2003/05 in the namespace
#   Interacts with scene7's backend to automate the process of finding assets, getting their size, ading them to a job queue
#   where the size < 1GB total and sending the jobs out for downloading.
#
#   XML content and exports from s7 need to be handled in the RAW not in the converted text. so response.content is the way to go



import requests, csv, os, getpass, xml.etree.ElementTree as ET
url = "https://s7sps1apissl.scene7.com/scene7/services/IpsApiService"

companyHandle = "c|8676"
masterU = "chris.string@turn5.com"
masterP = "Password2#"
loggedIn = False
sessionId = ""

#   authUser accepts username and password
def authUser(uname,pwd):
#    payload = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:ns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\">\r\n <soap:Header>\r\n <ns:authHeader>\r\n <!--Optional:-->\r\n <ns:user>{}</ns:user>\r\n <!--Optional:-->\r\n <ns:password>{}</ns:password>\r\n <ns:appName>bertz</ns:appName>\r\n <ns:appVersion>69</ns:appVersion>\r\n </ns:authHeader>\r\n </soap:Header>\r\n <soap:Body>\r\n <ns:checkLoginParam>\r\n <!--Optional:-->\r\n <ns:companyHandle>c|8676</ns:companyHandle>\r\n <ns:email>{}</ns:email>\r\n <ns:password>{}</ns:password>\r\n </ns:checkLoginParam>\r\n </soap:Body>\r\n</soap:Envelope>".format(masterU,masterP,uname,pwd)
#    headers = {'soapaction': "checkLogin",'cache-control': "no-cache"}

#    response = requests.request("POST", url, data=payload, headers=headers)

#   XML content and exports from scene7 payloads should be dealt with in the raw.

#    responseRoot = ET.fromstring(response.text)
    if uname=="chris.string@turn5.com" and pwd == "Password2#":
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


#   singleSkuSearch uses getAssetsByName
def singleSkuSearch(sku):
    #todo write rest of function
    print("searching s7 for: ",sku)


#======================= BEGIN TESTING HERE =============================

print("\t\t===Welcome to the Super Sweet Scene 7 Stuff Script===")
while loggedIn==False:
    print("Please provide your Scene 7 login credentials")
    inputUser = input("user email: ")
    inputPass = getpass.getpass("user password: ")

    if authUser(inputUser,inputPass):
        print("Credential check: PASS\nLogged In:")
        loggedIn=True
    else:
        print("Credential check: FAIL")
