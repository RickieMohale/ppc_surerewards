"""

	Simple Streamlit webserver application for serving developed classification
	models.

	Author: Explore Data Science Academy.

	Note:
	---------------------------------------------------------------------
	Please follow the instructions provided within the README.md file
	located within this directory for guidance on how to use this script
	correctly.
	---------------------------------------------------------------------

	Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend the functionality of this script
	as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
from ast import Str
import streamlit as st
import joblib,os

# Data dependencies
import pandas as pd

# graph in streamlit
import altair as alt
## For KPIS 
from streamlit_metrics import metric, metric_row

# MySQL 
#Import labraries
import pymysql


import warnings
warnings.filterwarnings("ignore")

## hiding warnings
st.set_option('deprecation.showPyplotGlobalUse', False)

## Ploting Labraries
import matplotlib.pyplot as plt
import matplotlib as mpl
import altair as alt



import numpy as np
import datetime



## Writing the latest time update
from datetime import datetime
import pytz

### Other tools
import operator


# import presentation packages 
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor



#########
import difflib

# Helpers to format and locate ticks for dates
from matplotlib.dates import DateFormatter, DayLocator
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter



#tweet_cv = joblib.load(news_vectorizer) # loading your vectorizer from the pkl file




# The main function where we will build the actual app

# Connecting To The Database Using MySQL
conn=pymysql.connect(host='us-mm-dca-d04d6c3c8e49.g5.cleardb.net',port=int(3306),user='b04c9045b8a037',passwd='f9f69807ebbcc01',db='heroku_c6143c8aee66786')


## Setting The Content To fill the Page
st.set_page_config(layout="wide")


def main():

	"""Tweet Classifier App with Streamlit """

	# Creates a main title and subheader on your page -
	# these are static across all pages


	# Loading Heading Images 


	## Function that automatically load images
	from PIL import Image



	
		
	st.sidebar.image("resources/imgs/surerewards.png", use_column_width=True)
	
	def load_image(image_file):
		img = Image.open(image_file)
		return img
	
	col1, col2, col3 = st.columns([1,20,1])

	with col1:
		st.write("")

	with col2:
		st.image("resources/imgs/Heading_Logo.PNG", use_column_width=True)
	with col3:
		st.write("")





	st.info("The following visuals are based on real time data from the surerewards platform (They change with time)")

	## Show the latest Update Time
	from datetime import datetime

	SA_time = pytz.timezone('Africa/Johannesburg') 
	datetime_SA = datetime.now(SA_time)
	metric("Latest Time Update", datetime_SA.strftime('%Y-%m-%d %H:%M %p'))

	def line_graph(source, x, y):
		# Create a selection that chooses the nearest point & selects based on x-value
		hover = alt.selection_single(fields=[x],nearest=True,on="mouseover",empty="none",	)

		lines = (alt.Chart(source).mark_line(point="transparent").encode(x=x, y=y).transform_calculate(color='datum.delta < 0 ? "red" : "green"'))

		# Draw points on the line, highlight based on selection, color based on delta
		points = (lines.transform_filter(hover).mark_circle(size=65).encode(color=alt.Color("color:N", scale=None)))

		# Draw an invisible rule at the location of the selection
		tooltips = (alt.Chart(source).mark_rule(opacity=0).encode(x=x,y=y,tooltip=[x, y, alt.Tooltip("delta", format=".2%")],).add_selection(hover))
		return (lines + points + tooltips).interactive()
	
	
	
	

    ### A function that takes a list and return unique name and their count
	def unique_names(list):
        
		unique={}
    
		for i in list:
			if i in unique.keys():
				unique[i] =unique[i]+1
			else:
				unique[i]=1
 		#sort using tuple
		tup =sorted(unique.items(), key=operator.itemgetter(1), reverse=True)
		dict_ = dict((x, y) for x, y in tup)
		return  dict_


	# senstivity is the percentange of senstivity

	def replace_similar_words(df,column,common_words,senstivity):
		for i,row in df.iterrows():
			for com_nam in common_words:
				if df.at[i,column] !=None and len(df.at[i,column]) >0 :
					if  df.at[i,column][0]==com_nam[0]:
						seq = difflib.SequenceMatcher(None,df.at[i,column] ,com_nam)
						if seq.ratio()*100>senstivity:
							df.at[i,column] =com_nam
						
		return df

	def convert_df(df):
		return df.to_csv().encode('utf-8')





	#st.subheader("Climate change tweet classification")

	# Creating sidebar with selection box -
	# you can create multiple pages this way
	
	options = ["Surerewards Customers", "Customer Profiling","Performance Target Page","Product Performance","Customer Location","Auto Reports"]
	#

	selection = st.sidebar.radio("Select Page:",options)
	#selection = st.sidebar.selectbox("Select Page", options)

	if selection == "Auto Reports":
		exec(open("./pages/auto_report_page.py").read())


	if selection == "Product Performance":
		exec(open("./pages/product_performance_page.py").read())





	if selection == "Customer Location":

		exec(open("./pages/customer_location_page.py").read())



	if selection == "Performance Target Page":

		exec(open("./pages/performance_target_page.py").read())

		
		
	if selection == "Customer Profiling":

		exec(open("./pages/customer_profile_page.py").read())





		#region_df = model_df[["region", 'Total number of bags']].groupby("region").describe()



		#st.dataframe(region_df)




		
			#st.info("The model trained is LSTM ( Long Short Term Memory) model,which falls under Recurrent Neural Network models. This model is a Time Series Model that uses historical data for forecasting/ predicting the number of bags in the upcoming 7 days")			
		

			








			






		

		

	if selection == "Surerewards Customers":

		exec(open("./pages/surerewards_customer_page.py").read())



# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
