from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  

model = tf.keras.models.load_model('path_to_your_model.h5') 
tokenizer = ... 
label_to_index = {
    "low": 0,
    "medium": 1,
    "high": 2
} 

def predict_urgency(symptoms):
    sequences = tokenizer.text
