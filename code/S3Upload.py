
""" 
Created on 02 October 2022
@author: Cipher 

In this module we are creating a function which can be used to upload files to an s3 bucket
by providing the function with the file name and bucket information etc.
"""

import boto3
import logging


logging.basicConfig(filename="./code/logs.txt", level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

s3_client = boto3.client("s3", region_name="ap-south-1", aws_access_key_id="AKIAZZXDASXGSGK7RFQR",
                         aws_secret_access_key="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")


def upload_output_file(bucket, folder, file_to_upload, file_name):
    """ The Function takes Four Inputs which are all strings 
        bucket: name of the S3 Bucket 
        folder: Name of the Folder to which you want to upload 
                the file inside the S3 bucket
        file_to_upload: location of the file that you want to upload 
        file_name: New name of the file that is being uploaded       
    """
    logging.debug("Entered upload_output_file methode Succesfully")

    key = folder+"/"+file_name
    try:
        response = s3_client.upload_file(file_to_upload, bucket, key)
        """ Here we are using a built in boto3 function to upload our file to the s3 bucket """
        
        logging.info("Output File Succesfully Uploaded to S3 bucket")
    except Exception as e:
        logging.error('''An Exception has occured while Uploading
                      the Output file to S3 bucket. Named : {}''', format(e))
        raise e



