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

# col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(12) #columnize the output
# with col4:
#     st.image("logo.png", width=300)

col = st.columns(24)[7]  # 7th column
with col:
    st.image("logo.png", width=300)


st.title("Patient Urgency Score Predictor")

st.markdown(
    """
    <p style="font-family: 'Garamond', serif; color: black; font-size: 16px;">
    <em> Note: This is for patients with Aetna insurance. If you carry a different type of insurance, please redirect to our home page. </em>
    </p>
    """,
    unsafe_allow_html=True
)


def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css()

model_path = 'model.keras' 
model = load_model(model_path)
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

st.markdown(
    """
    <style>
        .stTextInput label {
            color: #093b6d;
            font-family: 'Cambria', serif;
        }
        .stTextArea label {
            color: #093b6d;
            font-family: 'Cambria', serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# patient input
patient_id = st.text_input("Enter your patient ID:")
patient_name = st.text_input("Enter your name:")
patient_age = st.text_input("Enter your age:")
patient_symptoms = st.text_area("Describe your symptoms:")

if st.button("Submit"):

    urgency_score = predict_urgency(patient_symptoms, tokenizer, model)
    st.write(f"Predicted Urgency Score: {urgency_score}/5")
    
    predictions = [{"patient_ID": patient_id, "urgency_score": urgency_score}]
    df_new = pd.DataFrame(predictions)

    # add new row to csv
    #with open('test_data.csv', mode='a', newline='') as f:
    #    df_new.to_csv(f, header=False, index=False)
    with open('test_data.csv', mode='a', newline='') as f:
        # Write the new data as a single row
        f.write(f"{patient_id},{urgency_score}\n")
    
    
    st.write("Your information has been saved! Please check the phone number you have on file to confirm your appointment.")
