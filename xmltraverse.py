#!/usr/bin/env python3
# test the emergency XML broadcast system
from lxml import etree
print("running with lxml.etree")
#sampleXML =b"<?xml version='1.0' encoding='UTF-8'?><soapenv:Envelope xmlns:soapenv=\"http://www.w3.org/2003/05/soap-envelope\"><soapenv:Body><getAssetsByNameReturn xmlns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\"><assetArray><items><assetHandle>a|581084652</assetHandle><type>Image</type>\<name>T533729</name><lastModified>2018-03-30T20:00:50.234-05:00</lastModified><imageInfo><width>2000</width><height>1500</height></imageInfo></items><items><assetHandle>a|581083938</assetHandle><type>Image</type><name>T533729_alt1</name> <lastModified>2018-03-30T20:00:44.167-05:00</lastModified><imageInfo> <width>2000</width> <height>1500</height> </imageInfo> </items> <items> <assetHandle>a|581084637</assetHandle> <type>Image</type> <name>T533729_alt2</name> <lastModified>2018-03-30T20:00:49.404-05:00</lastModified> <imageInfo> <width>2000</width> <height>1500</height> </imageInfo> </items> </assetArray> </getAssetsByNameReturn> </soapenv:Body> </soapenv:Envelope>"

def parseMetaDataResponse(responseXML):
    print("parseMetaDataResponse function called")
    # TEST for no items found!
    root = etree.XML(responseXML, etree.XMLParser(remove_blank_text=True))
    #print(etree.dump(root))
    assetArray = root[0][0][0]
    _skuMetaData = []
    xmlNS = "{"+etree.QName(root[0][0]).namespace+"}"
    for item in assetArray.iter(xmlNS+"items"):
        #skdsuMetaData.append()
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
    print("Metadata Parsed, proceed.")
    return _skuMetaData
#======================= end parseMetaData========================


sampleXML=b"<soapenv:Envelope xmlns:soapenv=\"http://www.w3.org/2003/05/soap-envelope\"><soapenv:Body><getAssetsByNameReturn xmlns=\"http://www.scene7.com/IpsApi/xsd/2014-04-03\"><assetArray><items><assetHandle>a|581084652</assetHandle><type>Image</type><name>T533729</name><lastModified>2018-03-30T20:00:50.234-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>13115089</fileSize></imageInfo></items><items><assetHandle>a|581083938</assetHandle><type>Image</type><name>T533729_alt1</name><lastModified>2018-03-30T20:00:44.167-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>21931440</fileSize></imageInfo></items><items><assetHandle>a|581084637</assetHandle><type>Image</type><name>T533729_alt2</name><lastModified>2018-03-30T20:00:49.404-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>12999769</fileSize></imageInfo></items><items><assetHandle>a|581084651</assetHandle><type>Image</type><name>T533729_alt3</name><lastModified>2018-03-30T20:00:54.102-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>18121961</fileSize></imageInfo></items><items><assetHandle>a|581291012</assetHandle><type>Image</type><name>T533729_alt4</name><lastModified>2018-03-30T20:00:47.159-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>16856670</fileSize></imageInfo></items><items><assetHandle>a|581291023</assetHandle><type>Image</type><name>T533729_alt5</name><lastModified>2018-03-30T20:00:50.033-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>19262802</fileSize></imageInfo></items><items><assetHandle>a|581290219</assetHandle><type>Image</type><name>T533729_alt6</name><lastModified>2018-03-30T20:00:41.788-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>2000</width><height>1500</height><fileSize>19627961</fileSize></imageInfo></items><items><assetHandle>a|581291910</assetHandle><type>Image</type><name>T533729_alt15</name><lastModified>2018-03-30T20:00:48.836-05:00</lastModified><lastModifyUser>chris.string@turn5.com</lastModifyUser><imageInfo><width>810</width><height>608</height><fileSize>2007668</fileSize></imageInfo></items></assetArray></getAssetsByNameReturn></soapenv:Body></soapenv:Envelope>"

#================= end of xml structure =================

skuArray = parseMetaDataResponse(sampleXML)
print("Parsed Response Data:\r\n",*skuArray,sep="\n")
