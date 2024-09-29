import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def send_email(to_email, subject, body):
    from_email = "ayahzaheraldeen@gmail.com" 
    from_password = "your_app_password"   

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def predict_urgency(symptoms, tokenizer, model):
    sequences = tokenizer.texts_to_sequences([symptoms])
    X_input = pad_sequences(sequences, maxlen=100)
    
    prediction = model.predict(X_input)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    
    return predicted_class_index + 1  

st.title("Patient Urgency Score Predictor")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

model_path = 'model.keras' 
model = load_model(model_path)
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

patient_name = st.text_input("Enter your name:")
patient_age = st.text_input("Enter your age:")
patient_symptoms = st.text_area("Describe your symptoms:")
patient_email = st.text_input("Enter your email:")

if st.button("Submit"):
    urgency_score = predict_urgency(patient_symptoms, tokenizer, model)
    st.write(f"Predicted Urgency Score: {urgency_score}")


    predictions = [{"urgency_score": urgency_score, "email": patient_email}]
    df_new = pd.DataFrame(predictions)

    
    with open('test_data.csv', mode='a', newline='') as f:
        df_new.to_csv(f, header=f.tell() == 0, index=False)  # Write header only if file is empty

    st.write("Your information has been saved!")

    
    df_appointments = pd.read_csv('test_data.csv')  
    patient_appointment = df_appointments[df_appointments['email'] == patient_email]

    if not patient_appointment.empty:
        st.write("Your Appointment Details:")
        st.write(patient_appointment)

        
        confirm = st.button("Confirm Appointment")
        decline = st.button("Decline Appointment")

        if confirm:
            appointment_details = f"Dear {patient_name},\n\nYour appointment has been confirmed.\n\nBest regards,\nYour Clinic"
            send_email(patient_email, "Appointment Confirmation", appointment_details)
            st.success("Appointment confirmed and email sent!")

        elif decline:
            st.warning("You have declined the appointment.")
