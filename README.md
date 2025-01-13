# CampusCalm
Campus Calm is a web app designed to provide students with mental health resources and encourage them to track their daily moods.

Using Streamlit, an open-source Python framework, I created this web app that allows users to input their daily emotions, all within a convenient and aesthetically pleasing app. 

For storing the user's moods, I utilized a database using Google Sheets, which keeps track of their inputted moods, for up to 3 years. I connect the Sheet using the document link, and give streamlit the password information using the 'GSheetsConnection' library. 
