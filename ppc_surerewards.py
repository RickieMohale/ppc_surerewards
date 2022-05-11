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
	
	options = ["Surerewards Customers","Performance Target Page","Product Performance","Customer Location","Auto Reports"]
	#

	selection = st.sidebar.radio("Select Page:",options)
	#selection = st.sidebar.selectbox("Select Page", options)

	if selection == "Auto Reports":
		exec(open("./pages/auto_report_page.py").read())


	if selection == "Product Performance":
		exec(open("./pages/product_performance_page.py").read())





	if selection == "Customer Location":

		exec(open("./pages/customer_location_page.py").read())



	# Building out the "Information" page
	if selection == "Performance Target Page":

		
		
		st.markdown("<h3 style='text-align: center; color: black;'>This Page focuses on  setting dynamic daily targets </h3>", unsafe_allow_html=True)




		num_bags =pd.read_sql_query("select cast(r.createdAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  >= '2022-02-15'  group by date" ,conn)
		
		content = {'date': list(pd.to_datetime(num_bags['date'], errors='coerce')),'number_of_bags': list(num_bags['number_of_bags'])}
		df2 = pd.DataFrame(content).set_index('date')
		df2.sort_index(inplace=True)

		from statsmodels.tsa.seasonal import seasonal_decompose

		st.info("The number of bags by date is found to consist of two hidden properties, after decomposition the first property is a trend that shows that the number of bags bought by surerewards customers is increasing with time. The second property is that the number of bags  bought by surerewards customers has a weekly seasonality, that is it varies depending on the day of the week (with the weekend having the lowest sales ")


		if st.checkbox('Show trend'): # data is hidden if box is unchecked
			ax = seasonal_decompose(df2['number_of_bags'],period =7)

			fig =ax.plot()


			fig.set_size_inches((12, 9))
			# Tight layout to realign things
			fig.tight_layout()
			#plt.show()

			#results.plot();
			st.pyplot(fig)
		st.markdown("<h5 style='text-align: center; color: black;'>How the model works</h5>", unsafe_allow_html=True)


		#############  Load data ################


		df_receiptdata=pd.read_sql_query("SELECT location,cast(createdAt as date) as date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster,ppc_motor as ppc_mortar FROM receiptdata where cast(createdAt as date) >= '2022-02-15'" ,conn)
 
		df_receiptdata[['city','province']] = df_receiptdata['location'].str.split(',', expand=True)
		df_receiptdata.drop('location', axis=1, inplace=True)


		#Removing white spaces
		df_receiptdata['city'] = df_receiptdata['city'].str.strip() 
		df_receiptdata['province'] = df_receiptdata['province'].str.strip()


		#lowering all letters
		df_receiptdata['city'] =df_receiptdata['city'].str.lower()
		df_receiptdata['province'] = df_receiptdata['province'].str.lower()


		#Removing all punctuations

		df_receiptdata['city'] =df_receiptdata['city'].str.replace(r'[^\w\s]+', '', regex=True)
		df_receiptdata['province'] = df_receiptdata['province'].str.replace(r'[^\w\s]+', '', regex=True)

		
		#Removing all numbers from strings

		df_receiptdata['city'] =df_receiptdata['city'].str.replace('\d+', '', regex=True)
		df_receiptdata['province'] = df_receiptdata['province'].str.replace('\d+', '', regex=True)


		df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_mortar']

		## Taking posative Values
		df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

		df_receiptdata['ppc_mortar'] = df_receiptdata['ppc_mortar'].abs()


		#
		## Replacing wrong captured name with correct ones
		province_name =['limpopo','gauteng','mpumalanga','north west','free state','western cape','eastern cape','kwazulu natal','northern cape']


		##### Replacing province name with true province name ################3

		df_receiptdata=replace_similar_words(df_receiptdata,'province',province_name,80)


		##### Replacing incorrect province with mode


		prov_mode =df_receiptdata['province'].mode()[0]

		for i,row in df_receiptdata.iterrows():
			if df_receiptdata.at[i,'province'] not in province_name :
				df_receiptdata.at[i,'province'] =prov_mode
		

		coastal_prov = ['western cape','eastern cape','kwazulu natal','northern cape'] 

		df_receiptdata['region']=''

		for i,row in df_receiptdata.iterrows():
			if df_receiptdata.at[i,'province'] in coastal_prov:
				df_receiptdata.at[i,'region'] ='coastal'
			else :
				df_receiptdata.at[i,'region'] ='inland'



		###### inserting Weekday ####






		######## Model Data Frame  #############

		model_df =pd.DataFrame()
		model_df['date']=pd.to_datetime(df_receiptdata['date'], errors='coerce')
		model_df['region']  =df_receiptdata['region']
		model_df['Total number of bags']  =df_receiptdata['Total number of bags']

		model_df = model_df.groupby(['date','region']).agg({'Total number of bags':'sum'}).reset_index()

		model_df['weekday'] = model_df['date'].dt.day_name()




		
		
		
		








		#grouped_train =model_df.groupby(['date','weekday']).agg({'Total number of bags':'sum'}).reset_index()
		#grouped_train_ =model_df.groupby(['date','weekday'])['Total number of bags'].agg("sum")



		#if st.checkbox('Show data feed to the mode'):

		#	st.dataframe(model_df)

		


		

		if st.checkbox('Show Overall Weekday Performance Statistics'):
			region_df = model_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

			region_df  = region_df .astype(int)
			st.dataframe(region_df)

			csv = region_df.to_csv(index=True, sep=',')

			st.download_button(label="Download data as CSV",data=csv,file_name='Weekday Performance statistics.csv',mime='text/csv', )

		
		if st.checkbox('Show Inland Performance Statistics'):

			inland_df =model_df[model_df['region']=='inland']

			df_inland =inland_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

			df_inland = df_inland .astype(int)
			st.dataframe(df_inland)

			csv = df_inland.to_csv(index=True, sep=',')

			st.download_button(label="Download data as CSV",data=csv,file_name='Inland Performance statistics.csv',mime='text/csv', )


		if st.checkbox('Show Coastal Performance Statistics'):

			coastal_df =model_df[model_df['region']=='coastal']

			df_coastal =coastal_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

			df_coastal =df_coastal .astype(int)

			st.dataframe(df_coastal)

			csv = df_coastal.to_csv(index=True, sep=',')
			st.download_button(label="Download data as CSV",data=csv,file_name='Coastal Performance statistics.csv',mime='text/csv', )




		#region_df = model_df[["region", 'Total number of bags']].groupby("region").describe()



		#st.dataframe(region_df)




		
			#st.info("The model trained is LSTM ( Long Short Term Memory) model,which falls under Recurrent Neural Network models. This model is a Time Series Model that uses historical data for forecasting/ predicting the number of bags in the upcoming 7 days")			
		

			








			






		

		

	if selection == "Surerewards Customers":

		exec(open("./pages/surerewards_customer_page.py").read())



# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
