#!/usr/bin/env python3
# test the emergency XML broadcast system
from lxml import etree
print("running with lxml.etree")
sampleXML ='''<?xml version='1.0' encoding='UTF-8'?>
    <soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
        <soapenv:Body>
            <getAssetsByNameReturn xmlns="http://www.scene7.com/IpsApi/xsd/2014-04-03">
                <assetArray>
                    <items>
                        <assetHandle>a|581084652</assetHandle>
                        <type>Image</type>
                        <name>T533729</name>
                        <lastModified>2018-03-30T20:00:50.234-05:00</lastModified>
                        <imageInfo>
                            <width>2000</width>
                            <height>1500</height>
                        </imageInfo></items>
                    <items>
                        <assetHandle>a|581083938</assetHandle>
                        <type>Image</type>
                        <name>T533729_alt1</name>
                        <lastModified>2018-03-30T20:00:44.167-05:00</lastModified>
                        <imageInfo>
                            <width>2000</width>
                            <height>1500</height>
                        </imageInfo>
                    </items>
                    <items>
                        <assetHandle>a|581084637</assetHandle>
                        <type>Image</type>
                        <name>T533729_alt2</name>
                        <lastModified>2018-03-30T20:00:49.404-05:00</lastModified>
                        <imageInfo>
                            <width>2000</width>
                            <height>1500</height>
                        </imageInfo>
                    </items>
                    <items>
                        <assetHandle>a|581084651</assetHandle>
                        <type>Image</type>
                        <name>T533729_alt3</name>
                        <lastModified>2018-03-30T20:00:54.102-05:00</lastModified>
                        <imageInfo>
                            <width>2000</width>
                            <height>1500</height>
                        </imageInfo>
                    </items>
                </assetArray>
            </getAssetsByNameReturn>
        </soapenv:Body>
    </soapenv:Envelope>'''
#================= end of xml structure =================

#print(sampleXML)

root = etree.XML(sampleXML)
#etree.tostring(root)
