import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

def load_css(file_name):
    with open(file_name) as f:
        return f.read()

css = load_css('app.css') 
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown('<h1 class="title">Patient Appointment Scheduler</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your CSV file", type="csv", label_visibility="collapsed")

num_weeks = st.number_input("Enter number of weeks for appointment scheduling:", min_value=1, value=1)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df_sorted = df.sort_values(by='urgency_score', ascending=False)

    appointment_times = [
        "08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM",
        "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM"
    ]

    start_date = datetime.today()
    appointment_dates = []

    for i in range(len(df_sorted)):
        appointment_date = start_date + timedelta(days=random.randint(0, num_weeks * 7 - 1))
        appointment_dates.append(appointment_date.strftime('%Y-%m-%d'))  

    df_sorted['appointment_date'] = sorted(appointment_dates)
    df_sorted['appointment_time'] = [random.choice(appointment_times) for _ in range(len(df_sorted))]

    st.markdown('<h2 class="header">Sorted Patient List</h2>', unsafe_allow_html=True)
    st.write(df_sorted.to_html(classes='patient-list', index=False), unsafe_allow_html=True)
else:
    st.markdown('<div class="uploaded-file">Please upload a CSV file.</div>', unsafe_allow_html=True)
