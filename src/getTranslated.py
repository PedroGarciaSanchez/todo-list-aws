import json
import decimalencoder
import todoList
import boto3
import logging


def getTranslated(event, context):
    # IMP: para detectar el lenguaje:
    # https://docs.aws.amazon.com/comprehend/latest/dg/
    # get-started-api-dominant-language.html#get-started-api-dominant
    # -language-python
    # IMP!!! pag 61 de
    # https://docs.aws.amazon.com/es_es/translate/latest/dg/translate-dg.pdf
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    translate = boto3.client('translate')
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        # COMPREHEND: DETECTAR EL LENGUAJE CON BOTO
        comprehend = boto3.client(service_name='comprehend', region_name='region')
        record = json.dumps(item,cls=decimalencoder.DecimalEncoder)
        print('Calling DetectDominantLanguage')
        # print(json.dumps(comprehend.detect_dominant_language(Text = record),
        # sort_keys=True, indent=4))
        # supported languages:
        # https://docs.aws.amazon.com/comprehend/latest/dg/supported-languages.html
        source_language = json.dumps\
        (comprehend.detect_dominant_language(Text = record),\
        sort_keys=True, indent=4)
        print("Source language: " + source_language)
        print("End of DetectDominantLanguage\n")
        #response["Items"][0]['extension']
        target_language = event['pathParameters']['language']
        try:
            # The Lambda function calls the TranslateText operation and passes the
            # review, the source language, and the target language to get the
            # translated review.
            translatedResult = translate.translate_text(Text=record,
            SourceLanguageCode=source_language, TargetLanguageCode=target_language)
            logging.info("Translation output: " + str(translatedResult))
        except Exception as e:
            logger.error(response)
            raise Exception("[ErrorMessage]: " + str(e))
        response = {
            "statusCode": 200,
            # "body": json.dumps(item, cls=decimalencoder.DecimalEncoder)
            "body": translatedResult
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response

    
  # https://docs.aws.amazon.com/es_es/translate/latest/dg/translate-dg.pdf  
    
#     import logging
# import json
# import boto3
# import os
# translate = boto3.client('translate')
# dynamodb = boto3.client('dynamodb')
# firehose = boto3.client('firehose')
# TABLE_NAME = os.getenv('TABLE_NAME')
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# def lambda_handler(event, context):
#  logger.info(event)
# if 'source_language' in event and 'target_language' in event and 'review'
# in event and
#  'review_id' in event:
#  review_id = event['review_id']
#  source_language = event['source_language']
#  target_language = event['target_language']
#  review = event['review']
#  try:
#  # The Lambda function queries the Amazon DynamoDB table to check whether
#  # the review has already been translated. If the translated review
#  # is already stored in Amazon DynamoDB, the function returns it.
#  response = dynamodb.get_item(
#  TableName=TABLE_NAME,
#  Key={
#  'review_id': {
#  'N': review_id,
#  },
#  'language': {
#  'S': target_language,
#  },
#  }
#  )
#  logger.info(response)
#  if 'Item' in response:
#  return response['Item']['review']['S']
#  except Exception as e:
#  logger.error(response)
#  raise Exception("[ErrorMessage]: " + str(e))
