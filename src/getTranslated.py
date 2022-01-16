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
        comprehend = boto3.client(service_name='comprehend',
                                  region_name='us-east-1')
        record = json.dumps(item, cls=decimalencoder.DecimalEncoder)
        print('Calling DetectDominantLanguage')
        # PGS:
        # PGS: supported languages:
        # https://docs.aws.amazon.com/comprehend/latest/dg/
        # supported-languages.html
        source_language = json.dumps(
            comprehend.detect_dominant_language(Text=record),
            sort_keys=True,
            indent=4)
        print("Source language: " + source_language)
        languageCode = json.loads(source_language)
        code = (languageCode['Languages'][0]['LanguageCode'])
        print("LanguageCode: " + code)
        print("End of DetectDominantLanguage\n")
        target_language = event['pathParameters']['language']
        try:
            # The Lambda function calls the TranslateText operation and
            # passes the
            # review, the source language, and the target language to get the
            # translated review.
            translatedResult = translate.translate_text(
                Text=record,
                SourceLanguageCode=code,
                TargetLanguageCode=target_language)
            decoded = translatedResult.decode("utf-8").encode("windows-1252").decode("utf-8")
            # decoded = translatedResult.decode("utf-8"). \
            #                           encode("windows-1252").decode("utf-8")
            # logging.info("Translation output: " + str(translatedResult))
            # response = {
            #    "statusCode": 200,
            #    "body": str(translatedResult)
            # }
            logging.info("Translation output: " + str(decoded))
            response = {
                "statusCode": 200,
                "body": str(decoded)
            }
        except Exception as e:
            logger.error(item)
            raise Exception("[ErrorMessage]: " + str(e))
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
