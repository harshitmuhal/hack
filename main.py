import wikipedia
import re
import requests
from rake_nltk import Rake
from fastapi import FastAPI
import uvicorn

app=FastAPI()

def change_slang(slangText):
    prefixStr = '<div class="translation-text">'
    postfixStr = '</div'
    r = requests.post('https://www.noslang.com/', {'action': 'translate', 'p':
        slangText, 'noswear': 'noswear', 'submit': 'Translate'})
    startIndex = r.text.find(prefixStr) + len(prefixStr)
    endIndex = startIndex + r.text[startIndex:].find(postfixStr)
    return r.text[startIndex:endIndex]
 
def decontracted(phrase):
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase
 
@app.get('/get_phrases')
def get_phrases(text:str):
    #Removing contractions
    text_=decontracted(text)

    #Slang translation
    text_ += ' u'  # Its for not getting slang not found error
    text_=change_slang(text_)
    print(text_)
    text_=text_[:-4]

    #Important Phrases extraction
    rake_obj=Rake()
    text_=rake_obj.extract_keywords_from_text(text_)
    text_=rake_obj.get_ranked_phrases()
    return text_

@app.get('/get_information')
def get_information(topic:str):
    topic_list =wikipedia.search(topic)
    return wikipedia.summary(topic_list[0])

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
