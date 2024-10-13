import streamlit as st
import pandas as pd
from numpy.random import randint
from streamlit_gsheets import GSheetsConnection



st.set_page_config(page_title="Mood Tracker", page_icon= ":herb:" , layout="centered")

#@st.cache_data
st.cache_data.clear()
st.cache_resource.clear()
#from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Period")
#st.dataframe(data)

import calendar
from datetime import datetime

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go


#--------------------
moods = ["happy","sad","angry","excited","anxious","calm","tired","stressed","confused","bored","sick"]




st.title("Mood Tracker" +":potted_plant:")

#uses the datetime module to get the current year and previous and 
years = [datetime.now().year-1,datetime.now().year]
months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
dates = list(range(1,32))

#--------Database interface-----------


#---------navigation-----------
selected = option_menu(
    menu_title=None, options=["Enter Mood", "Overview"], orientation="horizontal", 
)
if selected == "Enter Mood":  
    st.header("How are you feeling today? Really.")
    with st.form(key='my_form', clear_on_submit=True):
        year = st.selectbox("Select Year",years, key="year")
        month = st.selectbox("Select Month",months, key="month")
        date = st.selectbox("Select Date",dates, key="date")
    
        "---"
        with st.expander("Mood"):
            for mood in moods:
                st.checkbox(mood, key=mood)
        with st.expander("Say more?"):
            st.text_area("Enter why here ...")

        "---"
        submitted = st.form_submit_button("Save")
        if submitted:
            period = str(st.session_state["year"]) + "-" + str(st.session_state["month"])
        
            moods = {mood : st.session_state[mood] for mood in moods}
            
            
        
        # add values into database
           
            data = conn.read(worksheet="Period")
            
            conn.update(data=data, worksheet="Period")
            st.cache_data.clear()
            st.cache_resource.clear()
            data.loc[len(data.index)] = [year, month, date, moods.get("happy"), moods.get("sad"), moods.get("angry"), moods.get("excited"), moods.get("anxious"), moods.get("calm"), moods.get("tired"), moods.get("stressed"), moods.get("confused"), moods.get("bored"), moods.get("sick")]
            #st.dataframe(data)
            conn.update(data=data, worksheet="Period")
            #st.write(period)
            #st.write(moods)
            st.write("Form submitted")
    
            #st.write("Mood saved")

#---------plot data-----------
if selected == "Overview":
    st.header("Mood Tracker Dashboard")
    with st.form("saved_periods"):
        period = st.selectbox("Select Date",["2024-January","2024-February","2024-March","2024-April","2024-May","2024-June","2024-July","2024-August","2024-September","2024-October","2024-November","2024-December"])
        submitted = st.form_submit_button("see data")
        if submitted:
            st.subheader("Data for " + period)
            if period == "2024-January":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                jan_data = conn.query("SELECT * FROM Period WHERE month = 'January' AND year = 2024")
                #st.write(jan_data)

                #find the sum of 'happy' values in jan_data
                sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'January' AND year = 2024")
                #convert the sum in the database to an integer
                sum_happy = (sum_happy_q.iloc[0,0]) *9
                positive = positive + sum_happy
                
                #sad
                sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'January' AND year = 2024")
                sum_sad = (sum_sad_q.iloc[0,0]) *2
                negative = negative - sum_sad
                #sum_sad = sum(jan_data["sad"])
                
                #angry
                sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'January' AND year = 2024")
                sum_angry = (sum_angry_q.iloc[0,0]) *2
                negative = negative - sum_angry
                
                #excited
                sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'January' AND year = 2024")
                sum_excited = (sum_excited_q.iloc[0,0]) *10
                positive = positive + sum_excited
                
                #anxious
                sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'January' AND year = 2024")
                sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                negative = negative - sum_anxious
                # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                
                #calm
                
                sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'January' AND year = 2024")
                sum_calm = (sum_calm_q.iloc[0,0]) * 6
                positive = positive + sum_calm
                
                #tired
                sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'January' AND year = 2024")
                sum_tired = (sum_tired_q.iloc[0,0]) * 4
                negative = negative - sum_tired
                
                #stressed
                sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'January' AND year = 2024")
                sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                negative = negative - sum_stressed
                
                #confused
                sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'January' AND year = 2024")
                sum_confused = (sum_confused_q.iloc[0,0]) * 4
                negative = negative - sum_confused
                
                #bored
                sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'January' AND year = 2024")
                sum_bored = (sum_bored_q.iloc[0,0]) * 5
                negative = negative - sum_bored
                
                #sick
                sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'January' AND year = 2024")
                sum_sick = (sum_sick_q.iloc[0,0]) *3
                negative = negative - sum_sick
                
                #determine if postive or negative is biggger
                
                
                labels = ['Postive','Negative']
                values = [positive,(-1) *negative]

                fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                st.plotly_chart(fig, use_container_width=True)
                
                #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
                
            elif period == "2024-February":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                feb_data = conn.query("SELECT * FROM Period WHERE month = 'February' AND year = 2024")
                #st.write(feb_data)

                #if query is empty, set sum to 0
                if feb_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'February' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'February' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-March":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                march_data = conn.query("SELECT * FROM Period WHERE month = 'February' AND year = 2024")
                #st.write(march_data)

                #if query is empty, set sum to 0
                if march_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'March' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'March' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-April":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                april_data = conn.query("SELECT * FROM Period WHERE month = 'February' AND year = 2024")
                #st.write(april_data)

                #if query is empty, set sum to 0
                if april_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'April' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'April' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-May":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                may_data = conn.query("SELECT * FROM Period WHERE month = 'February' AND year = 2024")
                #st.write(may_data)

                #if query is empty, set sum to 0
                if may_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'May' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'May' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-June":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                june_data = conn.query("SELECT * FROM Period WHERE month = 'June' AND year = 2024")
                #st.write(june_data)

                #if query is empty, set sum to 0
                if june_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'June' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'June' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-July":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                july_data = conn.query("SELECT * FROM Period WHERE month = 'July' AND year = 2024")
                #st.write(july_data)

                #if query is empty, set sum to 0
                if july_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'July' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'July' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-August":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                aug_data = conn.query("SELECT * FROM Period WHERE month = 'August' AND year = 2024")
                #st.write(aug_data)

                #if query is empty, set sum to 0
                if aug_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'August' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'August' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-September":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                sept_data = conn.query("SELECT * FROM Period WHERE month = 'September' AND year = 2024")
                #st.write(sept_data)

                #if query is empty, set sum to 0
                if sept_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'September' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'September' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-October":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                oct_data = conn.query("SELECT * FROM Period WHERE month = 'October' AND year = 2024")
                #st.write(oct_data)

                #if query is empty, set sum to 0
                if oct_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'October' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'October' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-November":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                nov_data = conn.query("SELECT * FROM Period WHERE month = 'November' AND year = 2024")
                #st.write(nov_data)

                #if query is empty, set sum to 0
                if nov_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'November' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'November' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                   
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            elif period == "2024-December":
                negative = 0
                positive = 0
                #grab all data from the database with january 2024
                december_data = conn.query("SELECT * FROM Period WHERE month = 'December' AND year = 2024")
                #st.write(december_data)

                #if query is empty, set sum to 0
                if december_data.empty:
                    st.write("No data for this period")
                    
                else:
                    #find the sum of 'happy' values in jan_data
                    sum_happy_q = conn.query("SELECT SUM(happy) FROM Period WHERE month = 'December' AND year = 2024")
                    #convert the sum in the database to an integer
                    sum_happy = (sum_happy_q.iloc[0,0]) *9
                    positive = positive + sum_happy
                    
                    #sad
                    sum_sad_q = conn.query("SELECT SUM(sad) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_sad = (sum_sad_q.iloc[0,0]) *2
                    negative = negative - sum_sad
                    #sum_sad = sum(jan_data["sad"])
                    
                    #angry
                    sum_angry_q = conn.query("SELECT SUM(angry) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_angry = (sum_angry_q.iloc[0,0]) *2
                    negative = negative - sum_angry
                    
                    #excited
                    sum_excited_q = conn.query("SELECT SUM(excited) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_excited = (sum_excited_q.iloc[0,0]) *10
                    positive = positive + sum_excited
                    
                    #anxious
                    sum_anxious_q = conn.query("SELECT SUM(anxious) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_anxious = (sum_anxious_q.iloc[0,0]) * 4
                    negative = negative - sum_anxious
                    # sum_anxious = (int)sum_anxious if sum_anxious is not None else 0
                    
                    #calm
                    
                    sum_calm_q = conn.query("SELECT SUM(calm) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_calm = (sum_calm_q.iloc[0,0]) * 6
                    positive = positive + sum_calm
                    
                    #tired
                    sum_tired_q = conn.query("SELECT SUM(tired) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_tired = (sum_tired_q.iloc[0,0]) * 4
                    negative = negative - sum_tired
                    
                    #stressed
                    sum_stressed_q = conn.query("SELECT SUM(stressed) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_stressed = (sum_stressed_q.iloc[0,0]) * 3
                    negative = negative - sum_stressed
                    
                    #confused
                    sum_confused_q = conn.query("SELECT SUM(confused) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_confused = (sum_confused_q.iloc[0,0]) * 4
                    negative = negative - sum_confused
                    
                    #bored
                    sum_bored_q = conn.query("SELECT SUM(bored) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_bored = (sum_bored_q.iloc[0,0]) * 5
                    negative = negative - sum_bored
                    
                    #sick
                    sum_sick_q = conn.query("SELECT SUM(sick) FROM Period WHERE month = 'December' AND year = 2024")
                    sum_sick = (sum_sick_q.iloc[0,0]) *3
                    negative = negative - sum_sick
                    
                    
                    
                    labels = ['Postive','Negative']
                    values = [positive,(-1) *negative]

                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    #reinforcing message
                if(positive > (-1) * negative):
                    st.write("You had such a great month! Keep it up! We are SO proud of you.")
                else:
                    st.write("You had a tough month. It's okay to have bad days. Remember to take care of yourself.")
            #data values  = {"happy":9,"sad":2,"angry":2,"excited":10,"anxious":4,"calm":6,"tired":3,"stressed":3,"confused":4,"bored":5,"sick":3}
        
            #create metrics
            #sum the values happy,excited,calm divided by number of true happy values for positive
        
        
            #plot data using plotly
        
            #make x equal to the number of days in the month depending on the month selected
            #TODO change w database addition
            month = "September"
            if month == "January" or month == "March" or month == "May" or month == "July" or month == "August" or month == "October" or month == "December":
                x = list(range(1,32))
            elif month == "April" or month == "June" or month == "September" or month == "November":
                x = list(range(1,31))
            else:
                x = list(range(1,29))
        
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x,
                y=[10 ,10, 9, 5, 8, 1, 10, 5, 9, 10, 5, None, 10, 6, 5, 1, 1, 5, 7, 10, None, 5, 10, 3, 5, 0, 10, None, 9, 5, 5],
               name = '<b>No</b> Gaps', # Style name/legend entry with html tags
               connectgaps=True # override default to connect the gaps
            ))
        
            #change size of plot
            fig.update_layout(
                margin=dict(l=0, r=0, t=5, b=5)
            )
            st.plotly_chart(fig, use_container_width=True)