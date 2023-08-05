import requests
import json

class SERVICE:

    def __init__(self, key):
        self._requestURL = "https://192.168.1.40:8011/"
        self._admin_token = "0qYusEEogCoi3yXhVChE6tThvnS5FwMMY69mBfYl"
        self._api_key = "Q7qrhf9dULZMuotdytoLH4MxpI9RXsEzCwBCvJvN"
        self._content_type = "application/json"    
        self._x_api_key = key

    def getHeader(self):
        headers = {}
        headers['X-Admin-Auth-Token'] = self._admin_token
        headers['X-Api-Key'] = self._api_key
        headers['Content-Type'] = self._content_type
        return headers

    def sentiment(self, text):
        url = self._requestURL + 'sentiment'
        data = {'text':text}
        try:
            response = requests.post(url=url, headers=self.getHeader(), json=data, verify=False)
            return response.json()
        except:
            return json.dumps({'Error':'Invalid data'})

    def similar_words(self, text):
        url = self._requestURL + 'similar_words'
        data = {'text':text, 'collection': 'BloombergandReuters'}
        try:
            respose = requests.post(url=url, headers=self.getHeader(), json=data, verify=False)
            return respose.json()
        except:
            return json.dumps({'Error':'No similar words found.'})

    def important_keywords(self, text):
        url = self._requestURL + 'important_keywords'
        data = {'text':text, 'collection': 'BloombergandReuters'}
        try:
            respose = requests.post(url=url, headers=self.getHeader(), json=data, verify=False)
            return respose.json()
        except:
            return json.dumps({'Error':'Zero important keywords found.'})

    def extractive_summary(self, text):
        url = self._requestURL + 'extractive_summary'
        data = {'text':text}
        try:
            respose = requests.post(url=url, headers=self.getHeader(), json=data, verify=False)
            return respose.json()
        except:
            return json.dumps({'Error':'Unable to find extractive summary.'})        

    def news_classification(self, news):
        url = self._requestURL + 'news_classification'
        data = {'news':news}
        try:
            respose = requests.post(url=url, headers=self.getHeader(), json=data, verify=False)
            return respose.json()
        except:
            return json.dumps({'Error':'Try with another news data.'})           
