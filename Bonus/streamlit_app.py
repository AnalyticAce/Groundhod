import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide", page_title="Temperature Analysis", page_icon="🌡️")
st.title('Upload your temperature data')

file_name = ''

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    st.success('Your data was uploaded successfully')
    
    if uploaded_file is not None:
        file_name = uploaded_file.name
else:
    st.warning('Please Upload your data before you proceed')

data = []
if uploaded_file is not None:
    for line in uploaded_file:
        try:
            value = float(line.decode().strip())
            data.append(value)
        except ValueError:
            pass
        
aberration_list = []
period_input = st.text_input('Enter a period')

if period_input != '':
    period = int(period_input)
    os.system(f"python3 bonus.py {period} < {file_name}")

    aberration_file = "file/aberration.txt"
    with open(aberration_file, "r") as file:
        for line in file:
            aberration_list.append(float(line.strip()))

    st.write("These are the aberrations in your data:", aberration_list)
else:
    st.warning("Please enter a period")

def plot_temparature(data, abbrev, period):
    df = pd.DataFrame(data, columns=['Temperature'])
    
    df['MA'] = df['Temperature'].rolling(window=period).mean()
    df['STD'] = df['Temperature'].rolling(window=period).std()
    df['Upper'] = df['MA'] + 2 * df['STD']
    df['Lower'] = df['MA'] - 2 * df['STD']
    df['MA_shifted'] = df['MA'].shift(1)
    df['Temperature_shifted'] = df['Temperature'].shift(1)
    
    df['Specified'] = df['Temperature'].where(df['Temperature'].isin(abbrev))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Temperature'], mode='lines', name='Temperature', line=dict(color='blue')))
    fig.add_trace(go.Scatter(y=df['MA'], mode='lines', name='Moving Average', line=dict(color='green')))
    fig.add_trace(go.Scatter(y=df['Upper'], mode='lines', name='Upper Bollinger Band', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(y=df['Lower'], mode='lines', name='Lower Bollinger Band', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(y=df['Specified'], mode='markers', name='Specified Temperatures', marker=dict(color='white', size=10)))
    
    fig.update_layout(autosize=True, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
button = st.button('Plot Aberration and temperature', key='plot_button', help='Click to plot the aberration and temperature')
if button:
    if period_input == "":
        st.warning("Please enter a period")
    else:
        plot_temparature(data, aberration_list, period)