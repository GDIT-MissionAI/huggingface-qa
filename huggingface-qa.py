from transformers import pipeline
import pandas as pd
import json
import boto3
import botocore
from base64 import b64encode

#load pipeline
nlp = pipeline("question-answering")

#load clients
s3Client = boto3.client('s3')

def lambda_handler(event, context):
  
    sQuestion = event.get("Question")
    sContext = event.get("Context")
    if (sContext = ""):
      sBucket = event.get("Bucket")
      sKey = event.get("Key")
    
    #event_dict = json.loads(event) #if "key" in "dict"
    #sSrcBucket = event["detail"]["ProcessOutputBucket"]
    #sSrcKey = event["detail"]["ProcessOutputKey"]
    #sSrcExtension = event["detail"]["ProcessExtension"]
    #sAssetId = event["detail"]["AssetId"]
    
    
