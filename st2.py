import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import pickle

# load tokenizer and model
def load_tokenizer(tokenizer_path):
    import pickle
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

#predicts urgency
def predict_urgency(symptoms, tokenizer, model):
    sequences = tokenizer.texts_to_sequences([symptoms])
    X_input = pad_sequences(sequences, maxlen=100)
    
    prediction = model.predict(X_input)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    
    return predicted_class_index + 1  # (1 to 5)

st.title("Patient Urgency Score Predictor")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

model_path = 'model.keras' 
model = load_model(model_path)
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)


# patient input
patient_name = st.text_input("Enter your name:")
patient_age = st.text_input("Enter your age:")
patient_id = st.text_input("Enter your ID:")
patient_symptoms = st.text_area("Describe your symptoms:")

if st.button("Submit"):

    urgency_score = predict_urgency(patient_symptoms, tokenizer, model)
    st.write(f"Predicted Urgency Score: {urgency_score}")
    
    predictions = [{"patient_ID": patient_id, "urgency_score": urgency_score}]
    df_new = pd.DataFrame(predictions)

    # add new row to csv
    with open('test_data.csv', mode='a', newline='') as f:
        df_new.to_csv(f, header=False, index=False)
    
    st.write("Your information has been saved!")