import wikipedia
import re
import requests
from rake_nltk import Rake
from fastapi import FastAPI
import uvicorn
import nltk
from textblob import TextBlob
from profanity_filter import ProfanityFilter

nltk.download('stopwords')
nltk.download('punkt')

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

    #spell check
    b=TextBlob(text_)
    text_=str(b.correct())

    #Important Phrases extraction
    rake_obj=Rake()
    text_=rake_obj.extract_keywords_from_text(text_)
    text_=rake_obj.get_ranked_phrases()

    return {'list':text_}

@app.get('/get_information')
def get_information(topic:str):
    try:
        text=wikipedia.summary(topic) 
    except wikipedia.exceptions.DisambiguationError as e:
        print(e.options[0])
        text=wikipedia.summary(e.options[0])
    return {'text':text}

@app.get('/detect_profanity')
def detect_profanity(text:str):
    pf = ProfanityFilter(languages=['en'])
    text=pf.censor(text)
    print(text)
    return {'text':text}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
