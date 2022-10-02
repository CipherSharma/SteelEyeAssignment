
""" 
Created on 02 October 2022
@author: Cipher 

In this module we are creating a function which can be used to filter specific data from a 
domtree elemnt object after which we obtain a set of donload links from which we donload 
some zip files and then extract all the data that is present in the zip file and store it 
in a seperate location named "XMLdata".

"""

import requests
import zipfile
import logging

logging.basicConfig(filename="./code/logs.txt", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")


def xml_extractor(group):
    logging.debug("Entered the xml_extractor Method")
    try:
        """Parsing through some specific tags using getElementsByTagName methode provided by minidom"""
        data = group.getElementsByTagName("doc")
        links = []
        for info in data:
            test = info.getElementsByTagName("str")
            link = None
            for i in test:
                """checking if the attrivute naem of the filtered tags according to provided constraints """
                if i.attributes["name"].value == "download_link":
                    """" using firstChild methode to obtain the first child tag of the current element object."""
                    """ using the data keyword to obtain the text data that is present in the tag."""
                    link = i.firstChild.data
                    """storing the links obtained in a python list"""
                    links.append(link)
                    
        logging.info("Succesfully Extracted all the Zip File Download Links")
    except Exception as e:
        logging.error('''An Exception has occured while Parsing 
                      the Downloaded XML file Named : {}''', format(e))
        raise e

    count = 1
    try:
        for i in links:
            """iterating through the python list in order to download the zip files 
            preset at those links """
            response = requests.get(i, stream=True)
            with open("./code/XMLdata{}.zip".format(count), "wb") as f:
                """Storing the downloaded zip file data in chunks"""
                for chunk in response.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
            count = count+1
        logging.info("all the zip files have been downloaded Succesfully")
    except Exception as e:
        logging.error('''An Exception has occured while Downloading  
                     the Zip files from the Obtained Links. Named : {}''', format(e))
        raise e
    
    count = 1
    """using count to iterate through all the downloaded zip files"""
    try:
        for i in links:
            with zipfile.ZipFile("./code/XMLdata{}.zip".format(count), "r") as zip_ref:
                """Extracting the downloaded zip files into a folder named "XMLdata". """
                zip_ref.extractall("./code/XMLdata/{}".format(count))
                count = count+1
        logging.info("all the zip files have been Extracted Succesfully")
    except Exception as e:
        logging.error('''An Exception has occured while Extracting   
                     the Download Zip files. Named : {}''', format(e))
        raise e
