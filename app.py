import numpy as np
import pandas as pd
import pickle
# import train_predict
from flask import Flask, jsonify, render_template, request,redirect, url_for
from flask_ngrok import run_with_ngrok
from train_predict import predict_all
import os
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# load the dataset but only keep the top n words, zero the rest

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# webapp
app = Flask(__name__, template_folder='./') 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# db = SQLAlchemy(app)
run_with_ngrok(app)

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():

    if  request.method == "POST":
        if 'file' not in request.files:
            return '<h2>No file given'

        f = request.files['file']
        print(f.filename)
        if f.filename != '':
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            result = predict_all(f.filename)
            print(result)
            return render_template('index.html', result=result)
    else:
        return render_template('index.html', result={})





if __name__ == '__main__':
    app.run()