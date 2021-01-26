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

for i in list_of_phrases:
	print(i)
	parameters={
		'topic':i
	}
	r=requests.get(url+'get_information',params=parameters)
	print(r.content)
	# summary=json.loads(r.content)
	# print(summary)

