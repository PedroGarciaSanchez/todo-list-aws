import http.client
import os
import unittest
from urllib.request import urlopen
import requests
import json

import pytest

# PGS: This BASE_URL is set in integration.sh, and before that, in the Jenkinsfile of each environment. i.e, for staging:
#https://f6l884sw05.execute-api.us-east-1.amazonaws.com/Prod

# BASE_URL = os.environ.get("BASE_URL")
# BASE_URL = "https://m0qwfec693.execute-api.us-east-1.amazonaws.com/Prod"
BASE_URL = "https://f6l884sw05.execute-api.us-east-1.amazonaws.com/Prod"
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    #PGS: we assert that the URL is not empty and has more than 8 characters
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")
        
        
        #PGS: LIST ALL RECORDS: ADD 1 RECORD AND LIST.

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        #Add TODO
        #PGS: we create a new row in the table, which we can consult later, at any moment
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        #PGS: We get the ID of the created record from the json of the response
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        #List
        url = BASE_URL+"/todos"
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertTrue(response.json())
        
        print('End - integration test List TODO')
    #PGS: ADD RECORD: add and delete by ID
    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        url = url+"/"+ID_TODO
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Add TODO')
        
    #PGS: GET RECORD: Create, get and delete
    def test_api_gettodo(self):
        print('---------------------------------------')
        print('Starting - integration test Get TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - GET"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - GET", "Error en la petición API a {url}"
        )
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - GET", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Get TODO')
        
        #PGS: UPDATE RECORD: add, update, get by id to check that the record has been correctly modified, and delete
    
    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        #Add TODO
        #PGS: We add a record
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Update TODO
        url = BASE_URL+"/todos/" + ID_TODO
        data = {
         "text": "Integration text example - Modified",
         "checked": "true"
        }
        #PGS: We use PUT to modify the text of the record and add a new attribute (checked)
        response = requests.put(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        #jsonbody= json.loads(json_response['body'])
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Test GET TODO
         #PGS: GET THE RECORD BY ID
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        #PGS: if the response status_code is not 200, make the test fail with a message
        #PGS: if the json of the response has not the content that we expect, make the test fail with a message
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        #PGS: We delete the record
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Update TODO')
        
        #PGS: DELETE RECORD: add, delete by id, and check with GET that the record does not exists anymore and the API returns HTTP 404
    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        #Add TODO
        #PGS: We add a record, get its id from te json of te response, and use that id to delete the record
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print ('Response Delete Todo:' + str(response))
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        print('Response Get Todo '+ url+': '+ str(response))
        self.assertEqual(
            response.status_code, 404, "Error en la petición API a {url}"
        )
        print('End - integration test Delete TODO')
    