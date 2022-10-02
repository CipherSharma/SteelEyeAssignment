""" 
Created on 02 October 2022
@author: Cipher 

In this module we are creating a function which can be used to covert the axtracted 
zip files into csv files ater extracting a specific set of information from them using 
Python module pandas.

"""

import pandas as pd
import logging

logging.basicConfig(filename="./code/logs.txt", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")



def write_to_csv(myLibrary):
    logging.debug("Entered the xml_extractor Method")
    """ Defining all the column names as specified in the documentation """
    cols = ["FinInstrmGnlAttrbts.Id", "FinInstrmGnlAttrbts.FullNm",
            "FinInstrmGnlAttrbts.ClssfctnTp", "FinInstrmGnlAttrbts.CmmdtyDerivInd", 
            "FinInstrmGnlAttrbts.NtnlCcy", "Issr"]
    rows = []
    
    try:
        """ Filtering to obtain the needed set of element objects """
        data = myLibrary.getElementsByTagName("FinInstrm")
        for info in data:
            """" using firstChild methode to obtain the first child tag of the current element object. """
            fin = info.firstChild.firstChild
            """using childNodes methode to obtain all the child nodes of the current element object. """
            """ using the data keyword to obtain the text data that is present in the tag."""
            id = fin.firstChild.childNodes[0].data
            full_nm = fin.childNodes[1].childNodes[0].data
            clssfctn_tp = fin.childNodes[3].childNodes[0].data
            ntnl_ccy = fin.childNodes[4].childNodes[0].data
            cmmdty_deriv_ind = fin.lastChild.childNodes[0].data
            issr = info.firstChild.childNodes[1].firstChild.data

            """ Adding the information obtained after filtering the xml file to a python dictionary"""
            rows.append({"FinInstrmGnlAttrbts.Id": id,
                        "FinInstrmGnlAttrbts.FullNm": full_nm,
                        "FinInstrmGnlAttrbts.ClssfctnTp": clssfctn_tp,
                        "FinInstrmGnlAttrbts.CmmdtyDerivInd": cmmdty_deriv_ind,
                        "FinInstrmGnlAttrbts.NtnlCcy": ntnl_ccy,
                        "Issr": issr
                        })
        """ Creating a pandas dataframe using rows and columns which we obtained before """
        df = pd.DataFrame(rows, columns=cols)
        """ converting the obtained dataframe into a csv file using the "to_csv" methode. """
        df.to_csv('./code/output1.csv', index=False)
        logging.info("Extracted XML file convereted to CSV")
    except Exception as e:
        logging.error('''An Exception has occured while Parsing 
                      the Extraced XML file Named : {}''', format(str(e)))
        raise e
