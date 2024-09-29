# Appoint AI -- HackGT Project

Appoint AI is a medical appointment triaging system. It calculates medical urgency based on a self-description of patient symptoms; then, prioritizing the highest-urgency patients, Appoint AI schedules the earliest available appointment for each patient.

This repository contains 3 folders: data, backend, and frontend.

**data**: the data folder contains all CSV files, including the data that was used to train the model, the data used to test the model, and the data collected when users submit the patient form.

**backend**: the backend folder contains the scripts to perform sentiment analysis, collect patient input (utilized to create the UI), and create the scheduling algorithm.

**frontend**: the frontend folder contains the .py scripts that use Streamlit to display webpages, as well as the data necessary for those .py scripts to run.
