from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load your trained model and tokenizer (adjust the path accordingly)
model = tf.keras.models.load_model('path_to_your_model.h5')  # Replace with your model path
tokenizer = ...  # Load your tokenizer here (e.g., using pickle or joblib)
label_to_index = {
    "low": 0,
    "medium": 1,
    "high": 2
}  # Adjust based on your urgency labels

# Function to predict urgency score based on input symptoms
def predict_urgency(symptoms):
    # Tokenize and pad the input symptoms
    sequences = tokenizer.text
