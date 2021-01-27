import requests
import json 

text="I want to know about menstruation"

url='https://hackvioletapi.herokuapp.com/'

parameters={
	'text':text
}

response=requests.get(url+'get_phrases',params=parameters)
list_of_phrases=json.loads(response.content)['list']
print(list_of_phrases)


parameters={
	'topic':'menstruation'
}
r=requests.get(url+'get_information',params=parameters)
summary=json.loads(r.content)
print(summary)

