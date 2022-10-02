""" 
Created on 02 October 2022
@author: Cipher 

In this Script We are importing all previously created function which are needed in order for us to download 
an xml file from a specified link then parse through the downloaded xml file and find specific links which 
are further used to download zip files.
After downloading the zip files we extract the xml files stored in the downloaded zip files and then we extract 
specific information form the extracted xml file which is then stored in a csv file. Which in the end is Stored 
in a S3 Bucket. 
"""
import requests
import logging
from xml.dom.minidom import parse   
"""Importing all the functions which we previously Created in order to complete the Task"""
from xml_to_csv import write_to_csv
from Extract_XML import xml_extractor
from S3Upload import upload_output_file

# Setting up my logging module
logging.basicConfig(filename="./code/logs.txt", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

URL = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"


try:
    """Downloading the xml file from the given Link """
    response = requests.get(URL)
    """Storing the Downloaded xml file"""
    open("./code/data.xml", "wb").write(response.content)
    
    logging.debug("XML file successfully downloaded")
    """Creating a Minidom Object to filter and parse the Downloadedxml file """
    domtree = parse("./code/data.xml")
    group = domtree.documentElement
    """Calling the xml_extrator method imported from Extract_XML.py"""
    xml_extractor(group)

    """Creating a Minidom Object to filter and parse the Extracted xml file """
    doc = parse("./code/XMLdata/1/DLTINS_20210117_01of01.xml")
    myLibrary = doc.getElementsByTagName("FinInstrmRptgRefDataDltaRpt")[0]

    """Calling the write_to_csv method imported from xml_to_csv.py """
    write_to_csv(myLibrary)

    """Calling the upload_output_file method imported from S3Upload.py """
    upload_output_file("ciphersharmabucket1", "Output",
                "./code/output1.csv", "output.csv")

    logging.info(" Script Ececuted Succesfully.....................")
    print("Script Executed Succesfully........")
except Exception as e:
    print("Exception occurded")
    logging.error("An Exception has Occured While Executing The Script.")
    raise e