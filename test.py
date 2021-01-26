import requests

text="I want to know about menstruation"

url='https://hackvioletapi.herokuapp.com/'

parameters={
	'text':text
}

response=requests.get(url+'get_phrases',params=parameters)
print(response.url)
print(response.content)