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

#Results
dfResult = ""

def lambda_handler(event, context):
    sQuestion = event.get("Question")
    sContext = event.get("Context")
    if (sContext == ""):
      sBucket = event.get("Bucket")
      sKey = event.get("Key")
      sContext = getContent(sBucket, sKey)
    
    #Get Results
    if sQuestion != "" and sContext != "": #Ensure values are populated
        dfResult = genAnswers(sQuestion, sContext, 11).to_string(header = True, index = False) #get answers
        print(dfResult)
        
    #event_dict = json.loads(event) #if "key" in "dict"
    #sSrcBucket = event["detail"]["ProcessOutputBucket"]
    #sSrcKey = event["detail"]["ProcessOutputKey"]
    #sSrcExtension = event["detail"]["ProcessExtension"]
    #sAssetId = event["detail"]["AssetId"]
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': dfResult.to_json() #return answers to caller
    }

#grab s3 object with text content
def getContent(srcBucket, srcKey):
    objContent = s3Client.get_object(Bucket=srcBucket, Key=srcKey)
    response = objContent['Body'].read()
    return response
  
#Generate the answers to the question.
def genAnswers(iquestion, icontext, topn):
    df = pd.DataFrame(nlp(question=iquestion, context=icontext, topk = topn, handle_impossible_answer=True))
    return df
#    for i in range(min(len(df), topn)):
#      df.iloc[i]["answer"]
#      #columns: answer, score, start, end
      
