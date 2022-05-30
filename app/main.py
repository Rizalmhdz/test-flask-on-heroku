#app/main.py
from flask import Flask, redirect, json, request
import pandas as pd
from keras.preprocessing import text, sequence
from keras.models import load_model
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/api/sms')

@app.route('/api/sms',methods=['GET'])
def get_json_sms():
    
    path = 'data/dataset_sms_spam_v1.csv'

    dataframe = pd.read_csv( path , encoding='iso8859')
    json = dataframe.to_json(orient='index')
                
    return json

@app.route('/predict' ,methods=['POST'])
def predict():
    user_input = [request.form.get('input')]
    path= str(Path().cwd()) +'\\CNN_model'
    model= load_model(path)

    
    max_features = 10000
    maxlen = 171
    label = ''
    output = []

        
    tokenizer = text.Tokenizer(num_words = max_features)
    tokenized_test = tokenizer.texts_to_sequences(user_input)
    user_input_tokenized = sequence.pad_sequences(tokenized_test, maxlen = maxlen)
    output = model.predict(user_input_tokenized)
    
    output = output[0][0]
        
    label = ''
        
    if output > 0.75 : 
        label = 'Berita Terindikasi sebagai Fakta'
    elif output <= 0.75 and output > 0.60 : 
        label = 'Berita Terindikasi lemah Fakta'
    elif output <= 0.6 and output > 0.5 :
        label = 'Berita perlu ditinjau ulang antara Fakta atau Hoax'
    elif output <= 0.5 and output > 0.35 : 
        label = 'Berita Terindikasi Lemah sebagai Hoax'
    elif output <= 0.35 and output > 0.15 : 
        label = 'Berita Terindikasi sebagai Hoax'
    elif output <= 0.15 :
        label = 'Berita Terindikasi Kuat sebagai Hoax'
        
    return json.dumps({'indicator': str(output),'msg' : label })


