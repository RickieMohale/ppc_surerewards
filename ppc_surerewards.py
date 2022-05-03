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

		st.info("This Page is for generating PPC130 reports.Time Frame Reports can be for weekly or weekend report")

		report_type=st.radio("Select Report Type",("Daily Report","Time Frame Report"))

		

		if report_type == "Daily Report":






			selected_date = st.date_input("Select Report Date")
			st.write('Your Selected Date is:',selected_date)



			### Raising Warning for trying to generate todays report ########
			
			
			from datetime import date
			today = date.today()

			#if selected_date ==today :
				#raise Exception("Sorry, you cannot generate todays report as receipts are being processed")
				#st.error("No frames fit the criteria. Please select different label or number.")

			#if selected_frame_index == None:
        	#	st.error("No frames fit the criteria. Please select different label or number.")
        	#	return




			num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) between '2022-02-15' and '"+ str(selected_date)+"' group by date order by date",conn)
					
			num_reg['date'] =  pd.to_datetime(num_reg['date'])


			sms_numbers=pd.read_sql_query("select count(*) as Number_Of_SMS_Sent ,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date) between '2022-02-15' and '"+ str(selected_date)+"' group by date order by date",conn)

			sms_numbers_on_date=pd.read_sql_query("select type,body,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date) between '2022-02-15' and '"+ str(selected_date)+"'",conn)


			Total_num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) = '"+ str(selected_date)+"' group by date order by date",conn)


			Total_num_reg =Total_num_reg['num_of_reg'].sum()



			status=pd.read_sql_query("select status, count(*) as count from users as u join receipts as r on u.id = r.user_id where cast(r.createdAt as date) = '"+ str(selected_date)+"' and status != 'unprocessed' group by status",conn)




			df_receiptdata=pd.read_sql_query("SELECT mechant,location,action as platform_massage,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) = '"+ str(selected_date)+"'" ,conn)

			camp_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) >= '2022-02-15' and cast(users.createdAt as date )<'"+str(selected_date)+"'",conn)
			camp_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) >= '2022-02-15' and cast(users.createdAt as date ) <'"+str(selected_date)+"'",conn)

			new_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) = '"+str(selected_date)+"'",conn)
			new_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) ='"+str(selected_date)+"'",conn)


			ex_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) < '2022-02-15'",conn)
			ex_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value  from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"'and cast(users.createdAt as date ) < '2022-02-15'",conn)










			bags_by_date=pd.read_sql_query("SELECT cast(updatedAt as date) as date ,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) between '2022-02-15' and '"+ str(selected_date)+"'" ,conn)
			bags_by_date['Total number of bags'] =bags_by_date['ppc_surebuild']+bags_by_date['ppc_surecem'] +bags_by_date['ppc_surecast']+bags_by_date['ppc_suretech']+bags_by_date['ppc_surewall']+bags_by_date['ppc_sureroad']+bags_by_date['ppc_plaster']+bags_by_date['ppc_motor']
			
			## Taking posative Values
			bags_by_date = bags_by_date[bags_by_date['Total number of bags']>0]
			bags_by_date['ppc_motor'] = bags_by_date['ppc_motor'].abs()


			num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) = '"+str(selected_date)+"' ",conn)
			num_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"' ",conn)

			num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code != 'PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) ='"+str(selected_date)+"' ",conn)
			num_valid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) = '"+str(selected_date)+"' ",conn)

			num_invalid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) = '"+str(selected_date)+"' ",conn)
			num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) = '"+str(selected_date)+"' ",conn)
					


			bags_by_date =bags_by_date.groupby(['date'])[['Total number of bags']].apply(lambda x : x.astype(int).sum())

			# Index to column
			bags_by_date= bags_by_date.reset_index(level=0)


			bags_by_date['date'] =  pd.to_datetime(bags_by_date['date'])



			df_receiptdata[['city','province']] = df_receiptdata['location'].str.split(',', expand=True)
			df_receiptdata.drop('location', axis=1, inplace=True)


			#Removing white spaces
			df_receiptdata['city'] = df_receiptdata['city'].str.strip() 
			df_receiptdata['province'] = df_receiptdata['province'].str.strip()
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.strip()

			#lowering all letters
			df_receiptdata['city'] =df_receiptdata['city'].str.lower()
			df_receiptdata['province'] = df_receiptdata['province'].str.lower()
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.lower()


			#Removing all punctuations

			df_receiptdata['city'] =df_receiptdata['city'].str.replace(r'[^\w\s]+', '', regex=True)
			df_receiptdata['province'] = df_receiptdata['province'].str.replace(r'[^\w\s]+', '', regex=True)
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace(r'[^\w\s]+', '', regex=True)

			
			#Removing all numbers from strings

			df_receiptdata['city'] =df_receiptdata['city'].str.replace('\d+', '', regex=True)
			df_receiptdata['province'] = df_receiptdata['province'].str.replace('\d+', '', regex=True)
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace('\d+', '', regex=True)			


			df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_motor']

			## Taking posative Values
			df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

			df_receiptdata['ppc_motor'] = df_receiptdata['ppc_motor'].abs()


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














			if st.button("Get "+ str(selected_date)+" Daily Report"):
				# Giving Image path 
				ppc_Logo_path ="resources/imgs/PPC_Logo.png" 

				top_left_path ="resources/imgs/top_left.png"
				bottom_right_path ="resources/imgs/bottom_right.png"

				small_logo_right_path ="resources/imgs/small_logo.png"

				surerewads_path ="resources/imgs/surerewards.png"

				analytics_path ="resources/imgs/AA_Logo.png"





				# Creating an Presentation object
				ppt = Presentation() 

				# set width and height to 16 and 9 inches.
				ppt.slide_width = Inches(16)
				ppt.slide_height = Inches(9)
				
				# Selecting blank slide
				blank_slide_layout = ppt.slide_layouts[6]


				################### First Slide #####################

				slide_one =st.empty()
				with slide_one:
				
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)


					left = Inches(1.409) 
					height = Inches(1) 
					top=Inches(2.291)

					pic = slide.shapes.add_picture(ppc_Logo_path, left,top,width=None, height=None)


					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(8.271)
					top=Inches(3.24)
					height = Inches(1.1969) 
					width = Inches(4.0118)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "PPC130 "
					p.font.bold = True
					p.font.size = Pt(65)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					################## Second Text     ###############################
					# For adjusting the Margins in inches
					
					left= Inches(7.531)
					top=Inches(4.583)
					height = Inches(0.6063) 
					width = Inches(6.083)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame
					#tf.text = "This is text inside a textbox"

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "Surerewards Daily Insights"
					p.font.bold = True
					p.font.size = Pt(30)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'



					################## Third Text Text     ###############################
					# For adjusting the Margins in inches
					
					left= Inches(8.437)
					top=Inches(5.1)
					height = Inches(0.7063) 
					width = Inches(3.681)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame
					#tf.text = "This is text inside a textbox"

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					x = pd.to_datetime(selected_date, format='%Y%m%d', errors='ignore')
					p.text =str(x.strftime("%Y-%d-%B"))
					p.font.bold = True
					p.font.size = Pt(30)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'


				#################### Report Outline ######################



				report_outline =st.empty()

				with report_outline :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4.94)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "Report Outline "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					############





					left= Inches(1)
					top=Inches(2.114)
					height = Inches(0.941) 
					width = Inches(5.181)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.text = ' > Customer Registration'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Date'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Products Sales By Province'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Store Location'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Region'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Merchant'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					

					

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Customer Receipts Upload'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Customer Engagement'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Receipts Validation'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

				
				####################  Customer Registration ################
				
				customer_reg=st.empty()

				with customer_reg :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Customer Registration "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################




					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( num_reg['date'] , num_reg['num_of_reg'] , color="red", alpha=0.2)
					plt.plot(num_reg['date'] , num_reg['num_of_reg'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function


					ax.set_ylabel('Number Of Registration')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/cust_reg'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					cust_reg ="resources/plots/cust_reg.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(cust_reg , left, top,width,height)


					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total of '+ str(Total_num_reg)+' customers registered on the surereward'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' platform  '+str(selected_date)
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


				### End of Reg ###


				#############  Number Of Bags By Date  ###############


				bags_by_=st.empty()

				with bags_by_ :
					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Sale By Date "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################

					




					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( bags_by_date['date'] , bags_by_date['Total number of bags'] , color="red", alpha=0.2)
					plt.plot(bags_by_date['date'] , bags_by_date['Total number of bags'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function





					ax.set_ylabel('Number Of Bags')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)


					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/bags_date'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					bags_date_img ="resources/plots/bags_date.png"



					pic = slide.shapes.add_picture(bags_date_img, left, top,width,height)


					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Surerewards customers bought a total of '+ str(bags_by_date['Total number of bags'][len(bags_by_date)-1])+' bags ' 
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' on the '+str(selected_date)
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

             	


				
				############ Product Split By Location ###############

				product_prov=st.empty()
				
				with product_prov :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Performance By Province"
					p.font.bold = True
					p.font.size = Pt(32)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################

					producd_region = df_receiptdata.groupby(['province'])['ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor'].sum().reset_index()

					product = pd.DataFrame({"ppc_surebuild":list(producd_region['ppc_surebuild']),'ppc_surecem':list(producd_region['ppc_surecem']),'ppc_surecast':list(producd_region['ppc_surecast']),'ppc_suretech':list(producd_region['ppc_suretech']),'ppc_surewall':list(producd_region['ppc_surewall']),'ppc_sureroad':list(producd_region['ppc_sureroad']),'ppc_plaster':list(producd_region['ppc_plaster']),'ppc_motor':list(producd_region['ppc_motor'])}, index=producd_region['province'])



					
					fig, ax = plt.subplots()
					plt.tight_layout()
					# Plotting the pie chart for above dataframe

					ax =product.plot(kind="bar",width=2)
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.legend(loc='best')

					ax.set_ylim(ymin =1)

					for container in ax.containers:
						ax.bar_label(container,rotation=90, padding=5)

					
					

					plt.savefig('resources/plots/product_loc'+'.png',bbox_inches='tight')
					
					left= Inches(1)
					top=Inches(2)
					height = Inches(6) 
					width = Inches(10)

					product_img ="resources/plots/product_loc.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(product_img  , left, top,width,height)











				#################   Performance By Store Location #############################

				store_location=st.empty()

				with store_location:


					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Sales By Store Location"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					############## Adding Merchant Performance

					#name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					#df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					#sorted_df=df.sort_values('Total number of bags', ascending=False)

					#mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					#data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					#mechant_freq_df = pd.DataFrame.from_dict(data)



					################# Top Performong Merchant By Sale Quantity
					name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					df =df_receiptdata.groupby(['city'])[name_].apply(lambda x : x.astype(int).sum())
					sorted_df=df.sort_values('Total number of bags', ascending=False)


					plot_df = sorted_df.head(20)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)


					fig, ax = plt.subplots()
					plt.tight_layout()	

					ax= plot_df.plot.barh(stacked=True)

					ax.set_xlim(left =1)
					for container in ax.containers:
						ax.bar_label(container, padding=5,label_type='center')

						

					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)



					# Label with label_type 'center' instead of the default 'edge'

					#ax.bar_label(label_type='center')

					#ax.bar_label(p2)




					ax.set_ylabel("Store Location")
					ax.set_xlabel("Number Of Bags")

					plt.savefig('resources/plots/'+'top_city.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_city_by_no ="resources/plots/top_city.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_city_by_no , left, top,width,height)


                    ############### Top city by sales  frequency
					mechant_freq_dict = unique_names(df_receiptdata['city'])
					data = {'Store Location': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					mechant_freq_df = pd.DataFrame.from_dict(data)


					plot_df =mechant_freq_df.head(20)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					bars = ax.barh(list(plot_df['Store Location']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					
					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					plt.ylabel('Store Location')
					plt.xlabel('Sales Frequency')


					plt.savefig('resources/plots/'+'top_city_by_freq.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_city_by_freq ="resources/plots/top_city_by_freq.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_city_by_freq , left, top,width,height)


					################ Adding Comment #######################

					# creating textBox
					left= Inches(1)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the left shows top 20 performing store location by product and the total number of bags'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the right shows top 20 performing store location by the number of customers who made sales'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'




			 
			 
			 
			 
			 	#############  Region Contribution ###################

			 
				region_=st.empty()

				with region_ :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Performance By Region "
					p.font.bold = True
					p.font.size = Pt(32)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################


					
					fig, ax = plt.subplots(figsize=(10, 6))

					# Plotting the pie chart for above dataframe
					ax = df_receiptdata.groupby(['region']).sum().plot(kind='pie', y='Total number of bags', autopct='%1.0f%%')
					 

					



					plt.savefig('resources/plots/region_perc'+'.png',bbox_inches='tight')
					
					left= Inches(1)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(4)

					region_perc_img ="resources/plots/region_perc.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(region_perc_img  , left, top,width,height)



					#######################    Adding Second  Plot ##########################


					fig, ax = plt.subplots(figsize=(10, 6))



					
					# Plotting the pie chart for above dataframe
					ax = df_receiptdata.groupby(['region']).sum().plot(kind='bar', y='Total number of bags')


					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					
					for container in ax.containers:
						ax.bar_label(container,rotation=90, padding=5)

					

					
					
	


					plt.savefig('resources/plots/region_sum'+'.png',bbox_inches='tight')
					
					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(4)

					region_sum_img ="resources/plots/region_sum.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(region_sum_img  , left, top,width,height)


					#######################################################################



					sum_region =df_receiptdata.groupby(['region'])['Total number of bags'].sum().reset_index()

					coastal_bags = sum_region.loc[sum_region['region'] =='coastal']['Total number of bags'].item()

					inland_bags = sum_region.loc[sum_region['region'] =='inland']['Total number of bags'].item()




					# creating textBox
					left= Inches(3)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Inland contributed   '+ str(inland_bags)+' bags , translating to '+str((inland_bags*50)/1000) +' tons of cement.'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.text = '> Coastal ranked in '+str(coastal_bags )+' bags of PPC cement translating to '+str((coastal_bags*50)/1000)+' tons of cement.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					
			 ######################################################



					#pic = slide.shapes.add_picture(chart, left,top)

                ################### Top Performing Merchant ############

				Merchant_pef=st.empty()

				with Merchant_pef:


					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Top 20 Performing Merchant"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					############## Adding Merchant Performance

					#name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					#df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					#sorted_df=df.sort_values('Total number of bags', ascending=False)

					#mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					#data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					#mechant_freq_df = pd.DataFrame.from_dict(data)



					################# Top Performong Merchant By Sale Quantity
					name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					sorted_df=df.sort_values('Total number of bags', ascending=False)


					plot_df = sorted_df.head(20)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)


					ax = plot_df.plot.barh(stacked=True)
					plt.tight_layout()		

					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.set_ylabel("Merchant")
					ax.set_xlabel("Number Of Bags")
					
					ax.set_xlim(1,)
					for container in ax.containers:
						ax.bar_label(container, padding=5,label_type='center')


					plt.savefig('resources/plots/'+'top_mecharnt_by_no.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_mecharnt_by_no ="resources/plots/top_mecharnt_by_no.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_mecharnt_by_no , left, top,width,height)


                    ############### Top Mechart by sales  frequency
					mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					mechant_freq_df = pd.DataFrame.from_dict(data)


					plot_df =mechant_freq_df.head(20)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					bars = ax.barh(list(plot_df['merchant']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')


					plt.ylabel('Merchant')
					plt.xlabel('Sales Frequency')


					plt.savefig('resources/plots/'+'top_mecharnt_by_freq.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_mecharnt_by_freq ="resources/plots/top_mecharnt_by_freq.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_mecharnt_by_freq , left, top,width,height)


					################ Adding Comment #######################

					# creating textBox
					left= Inches(1)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the left shows top 20 merchant performing by product and the total number of bags'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the right shows top 20 merchant performance by the number of customers who made sales'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

                ##########  Receipts Upload  ######################


				recpt_upload=st.empty()

				with recpt_upload:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Receipt Upload"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					############ Adding Plot #################


		
					N = 3
					No_Promo = (num_receipts['no_of_receipts_upload'].sum(), num_valid_receipts["no_of_valid_receipts"].sum(), num_invalid_receipts["no_of_invalid_receipts"].sum()  )
					Promo = (num_promo_receipts['no_of_receipts_upload'].sum(), num_valid_promo_receipts["no_of_valid_receipts"].sum(),num_invalid_promo_receipts["no_of_invalid_receipts"].sum())
					
					ind = np.arange(N)    # the x locations for the groups
					width = 0.35       # the width of the bars: can also be len(x) sequence



					fig, ax = plt.subplots()
					plt.tight_layout()

					p1 = ax.bar(ind, Promo, width,  label='With PPC130')
					p2 = ax.bar(ind, No_Promo, width,bottom=Promo, label='Without PPC130')

					ax.axhline(0, color='grey', linewidth=0.8)
					ax.set_ylabel('Number Of Receipts ')
					

					ax.set_xticks(ind,labels=['Total', 'Valid', 'Invalid'])
					ax.legend()

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Label with label_type 'center' instead of the default 'edge'
					ax.bar_label(p1, label_type='center')
					ax.bar_label(p2, label_type='center')
					#ax.bar_label(p2)


					plt.savefig('resources/plots/'+'receipt_upload.png',bbox_inches='tight')
					


					left= Inches(0.5)
					top=Inches(2)
					height = Inches(5.5) 
					width = Inches(6)

					receipt_upload_path ="resources/plots/receipt_upload.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(receipt_upload_path , left, top,width,height)


					############# Adding Comments #################################333

					# creating textBox
					left= Inches(6.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total of '+ str(num_receipts['no_of_receipts_upload'].sum()+num_promo_receipts['no_of_receipts_upload'].sum())+' receipts were uploaded on the '+str(selected_date)
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '> Out of the total receipts uploaded,'+str(num_valid_receipts["no_of_valid_receipts"].sum()+num_valid_promo_receipts["no_of_valid_receipts"].sum())+ ' were found to be valid and thus approved'
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > From the valid receipts, '+str(num_valid_receipts["no_of_valid_receipts"].sum())+' did not have PPC130 promo code'
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > '+str( num_invalid_receipts["no_of_invalid_receipts"].sum()+num_invalid_promo_receipts["no_of_invalid_receipts"].sum())+ ' invalid receipts were uploaded, '+str(num_invalid_receipts["no_of_invalid_receipts"].sum())+' did not have PPC130 promo code.'

					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'



				################### Customer Engagement #################

				customer_eng=st.empty()

				with customer_eng:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Customer Engagement"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					############ Adding Plot #################	

					
					fig, ax = plt.subplots()
					plt.tight_layout()

					users_ = ["New Users","Users From Campaign","Existing Users"]
				
					no_receipts = [new_u_recpt['value'].item(),camp_u_recpt['value'].item(), ex_u_recpt['value'].item()]


					# Plot horizontal bar chart

					bars = plt.barh(users_ ,no_receipts)

					# To get data labels

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
						
					# Define axes labels

					plt.xlabel("No Of Receipts ")


					plt.savefig('resources/plots/'+'user_recpt.png',bbox_inches='tight')
					

					receipt_user_path ="resources/plots/user_recpt.png"

					left= Inches(0.5)
					top=Inches(2)
					height = Inches(3) 
					width = Inches(6)
					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(receipt_user_path  , left, top,width,height)


					#### Second Visual #############

					fig, ax = plt.subplots()
					plt.tight_layout()

					users_ = ["New Users","Users From Campaign","Existing Users"]

					no_user = [new_u_numb['value'].item(),camp_u_numb['value'].item(), ex_u_numb['value'].item()]


					# Plot horizontal bar chart

					bars = plt.barh(users_ ,no_user)

					# To get data labels

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
						
					# Define axes labels

					plt.xlabel("No Of Users ")


					plt.savefig('resources/plots/'+'user_no.png',bbox_inches='tight')
					

					no_user_path ="resources/plots/user_no.png"

					left= Inches(8)
					top=Inches(2)
					height = Inches(3) 
					width = Inches(6)





					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(no_user_path  , left, top,width,height)

					################## Add Comments #################

				    # creating textBox
					left= Inches(3)
					top=Inches(5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)


					total_recpt = num_receipts['no_of_receipts_upload'].sum()+num_promo_receipts['no_of_receipts_upload'].sum()
					new_u_perc =round((new_u_recpt['value'].item()/total_recpt)*100)
					ex_u_perc= round((ex_u_recpt['value'].item()/total_recpt)*100)
					camp_u_perc = round((camp_u_recpt['value'].item()/total_recpt)*100)


					p.text = ' > Out of the total '+str(total_recpt )+ ' receipts uploads, '+str(new_u_perc)+'% was from New Users ( registered on '+str(selected_date)+ ' ).'

					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(camp_u_perc)+'% of receipts uploads was from Users From Campaign ( registered from the 15 February to'+str(selected_date) +' ).'

					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(ex_u_perc)+'% of the receipts was from Existing Users( registered before 15 February 2022).'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > From the '+str(Total_num_reg)+' customer registration , '+str(new_u_numb['value'].item())+' customers uploaded receipts ( Customer conversion of '+str(round((new_u_numb['value'].item()/Total_num_reg)*100))+'%).'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'







				###### Receipt Validation ##########


				recpt_validation=st.empty()

				with recpt_validation:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Receipt Validation"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					##### placing the figure #######

					fig, ax = plt.subplots()
					plt.tight_layout()

					sizes = list(status['count'])

					# Setting labels for items in Chart
					labels = list(status['status'])

					# colors
					

					# explosion
					

					# Pie Chart
					ax =plt.pie(sizes, labels=labels,autopct='%1.1f%%', pctdistance=0.85)

					# draw circle
					centre_circle = plt.Circle((0, 0), 0.70, fc='white')
					fig = plt.gcf()

					# Adding Circle in Pie chart
					fig.gca().add_artist(centre_circle)


					plt.savefig('resources/plots/'+'status_plot.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(5) 
					width = Inches(7)

					status_img ="resources/plots/status_plot.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(status_img , left, top,width,height)



					###### Adding Comments ##########################3

					apprv_ = status[status['status']=='approved']['count'].reset_index()
					limit_ = status[status['status']=='Limit reached.']['count'].reset_index()

					apprvd_per =round(((apprv_['count'][0]+limit_['count'][0])/status['count'].sum())*100,2)



					
					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+ str(apprvd_per )+'% of the receipts uploaded were found to be valid and thus were approved,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = 'Limit reached included'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+ str(round(100-apprvd_per,2))+'% of the receipts were not approved'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > The main reasons for disapproval includes, Receipt not visible , Receipt not relevant'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' Duplicate receipt and Outdated receipt.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

				######## Communication By SMS  ##############

				comm_sms=st.empty()

				with comm_sms:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Customer Communication By SMS"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					###### Add Plots ########

					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( sms_numbers['date'] , sms_numbers['Number_Of_SMS_Sent'] , color="red", alpha=0.2)
					plt.plot(sms_numbers['date'] , sms_numbers['Number_Of_SMS_Sent'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function


					ax.set_ylabel('Number Of SMS Sent')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/cust_sms'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(1.5)
					height = Inches(4) 
					width = Inches(7)

					cust_sms ="resources/plots/cust_sms.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(cust_sms , left, top,width,height)





					#########################


					
					# creating textBox
					left= Inches(8)
					top=Inches(2)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total  of '+ str( sms_numbers['Number_Of_SMS_Sent'].sum() )+' SMS where sent between 15 Feb  2022 and '+ str(selected_date)
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'




					total_sms_date =len(list(sms_numbers_on_date['body']))
					withdrawm_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('withdraw')]['body'].count()
					succes_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('successfully captured')]['body'].count()
					less_bag_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('Miss Out')]['body'].count()

 

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > From the SMS sent ,'+str(withdrawm_no)+' was SMS about withdrawal request,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((withdrawm_no/total_sms_date)*100))+'% of the total SMS sent. '
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(succes_no )+' was SMS about successfully captured receipts,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((succes_no/total_sms_date)*100))+'%  of the total SMS sent.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(less_bag_no)+' was SMS sent to customers who bought less than 10 bags, '
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((less_bag_no/total_sms_date)*100))+'%  of the total SMS sent.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					################ Botttom Comments ####################



					left= Inches(5) 
					top=Inches(5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' Types Of SMS'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(225, 0, 0)
					p.font.name = 'Arial'







					left= Inches(1) 
					top=Inches(5.5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 1) Request to withdraw is received and will be processed within 24 hours to the following account:'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 2) Your receipt has been successfully captured and Well Done! You have successfully been entered into our daily draw to win R 10 000 CASH'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 3) Don’t Miss Out!. Purchase 10 bags or more, Apply Promo Code PPC130 on SUREREWARDS and STAND A CHANCE TO WIN R 10 000'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'



                ############ Last Slide  ###############
				last_slide=st.empty()

				with last_slide:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

	


					left= Inches(5)
					top=Inches(0.5)
					height = Inches(6) 
					width = Inches(6)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)






					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					left= Inches(5.5)
					top=Inches(6)
					height = Inches(0.941) 
					width = Inches(5.181)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame



					p = tf.add_paragraph()

					p.text = 'THANK YOU'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(60)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					 




					






                ##  Saving  to file
				#ppt.save('Daily Report.pptx')

				#f = open('Daily Report.pptx','r')


				#########   Downloading the Presentation #######

				from io import BytesIO


				# save the output into binary form
				binary_output = BytesIO()
				ppt.save(binary_output) 

				st.download_button(label = 'Download Daily Report',data = binary_output.getvalue(),file_name = str(selected_date)+' Daily Report.pptx')

		
		
		##################### Time Frame Interval #######################################
		################################################################################
		if report_type == "Time Frame Report":
			start_date = st.date_input("Select Report Start Date")
			end_date = st.date_input("Select Report End Date")

			st.write('Your Selected Date is from :',start_date,' to ',end_date)




			num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) between '2022-02-15' and '"+ str(end_date)+"' group by date order by date",conn)
					
			num_reg['date'] =  pd.to_datetime(num_reg['date'])


			sms_numbers=pd.read_sql_query("select count(*) as Number_Of_SMS_Sent ,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date) between '2022-02-15' and '"+ str(end_date)+"' group by date order by date",conn)

			sms_numbers_on_date=pd.read_sql_query("select type,body,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date) between '2022-02-15' and '"+ str(end_date)+"'",conn)


			Total_num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date)  between '"+ str(start_date)+"' and '"+ str(end_date)+"' group by date order by date",conn)


			Total_num_reg =Total_num_reg['num_of_reg'].sum()



			status=pd.read_sql_query("select status, count(*) as count from users as u join receipts as r on u.id = r.user_id where cast(r.createdAt as date) between '"+ str(start_date)+"' and '"+ str(end_date)+"' and status != 'unprocessed' group by status",conn)




			df_receiptdata=pd.read_sql_query("SELECT mechant,location,action as platform_massage,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) between '"+ str(start_date)+"' and '"+ str(end_date)+"'" ,conn)

			camp_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) >= '2022-02-15' and cast(users.createdAt as date )<'"+str(start_date)+"'",conn)
			camp_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) >= '2022-02-15' and cast(users.createdAt as date ) <'"+str(start_date)+"'",conn)

			new_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) between '"+ str(start_date)+"' and '"+ str(end_date)+"'",conn)
			new_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) between'"+ str(start_date)+"' and '"+ str(end_date)+"'",conn)


			ex_u_recpt = pd.read_sql_query( "SELECT count(users.id) as value from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) < '2022-02-15'",conn)
			ex_u_numb = pd.read_sql_query( "SELECT count(distinct(users.id)) as value  from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"'and cast(users.createdAt as date ) < '2022-02-15'",conn)










			bags_by_date=pd.read_sql_query("SELECT cast(updatedAt as date) as date ,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) between '2022-02-15' and '"+ str(end_date)+"'" ,conn)
			bags_by_date['Total number of bags'] =bags_by_date['ppc_surebuild']+bags_by_date['ppc_surecem'] +bags_by_date['ppc_surecast']+bags_by_date['ppc_suretech']+bags_by_date['ppc_surewall']+bags_by_date['ppc_sureroad']+bags_by_date['ppc_plaster']+bags_by_date['ppc_motor']
			
			## Taking posative Values
			bags_by_date = bags_by_date[bags_by_date['Total number of bags']>0]
			bags_by_date['ppc_motor'] = bags_by_date['ppc_motor'].abs()


			num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) between '"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)
			num_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)

			num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code != 'PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)
			num_valid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)

			num_invalid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) between '"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)
			num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) between'"+ str(start_date)+"' and '"+ str(end_date)+"' ",conn)
					


			bags_by_date =bags_by_date.groupby(['date'])[['Total number of bags']].apply(lambda x : x.astype(int).sum())

			# Index to column
			bags_by_date= bags_by_date.reset_index(level=0)


			bags_by_date['date'] =  pd.to_datetime(bags_by_date['date'])



			######## bags inter #########################

			bags_interval=pd.read_sql_query("SELECT cast(updatedAt as date) as date ,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) between '"+str(start_date)+"' and '"+ str(end_date)+"'" ,conn)
			bags_interval['Total number of bags'] =bags_interval['ppc_surebuild']+bags_interval['ppc_surecem'] +bags_interval['ppc_surecast']+bags_interval['ppc_suretech']+bags_interval['ppc_surewall']+bags_interval['ppc_sureroad']+bags_interval['ppc_plaster']+bags_interval['ppc_motor']
			
			## Taking posative Values
			bags_interval = bags_interval[bags_interval['Total number of bags']>0]
			bags_interval['ppc_motor'] =bags_interval['ppc_motor'].abs()

			
			bags_interval =bags_interval.groupby(['date'])[['Total number of bags']].apply(lambda x : x.astype(int).sum())

			# Index to column
			bags_interval=bags_interval.reset_index(level=0)


			bags_interval['date'] =  pd.to_datetime(bags_interval['date'])


			######################################



			df_receiptdata[['city','province']] = df_receiptdata['location'].str.split(',', expand=True)
			df_receiptdata.drop('location', axis=1, inplace=True)


			#Removing white spaces
			df_receiptdata['city'] = df_receiptdata['city'].str.strip() 
			df_receiptdata['province'] = df_receiptdata['province'].str.strip()
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.strip()

			#lowering all letters
			df_receiptdata['city'] =df_receiptdata['city'].str.lower()
			df_receiptdata['province'] = df_receiptdata['province'].str.lower()
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.lower()


			#Removing all punctuations

			df_receiptdata['city'] =df_receiptdata['city'].str.replace(r'[^\w\s]+', '', regex=True)
			df_receiptdata['province'] = df_receiptdata['province'].str.replace(r'[^\w\s]+', '', regex=True)
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace(r'[^\w\s]+', '', regex=True)

			
			#Removing all numbers from strings

			df_receiptdata['city'] =df_receiptdata['city'].str.replace('\d+', '', regex=True)
			df_receiptdata['province'] = df_receiptdata['province'].str.replace('\d+', '', regex=True)
			df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace('\d+', '', regex=True)			


			df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_motor']

			## Taking posative Values
			df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

			df_receiptdata['ppc_motor'] = df_receiptdata['ppc_motor'].abs()


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












			if st.button("Get "+ str(start_date)+' to '+str(end_date)+" Report"):
				# Giving Image path 
				ppc_Logo_path ="resources/imgs/PPC_Logo.png" 

				top_left_path ="resources/imgs/top_left.png"
				bottom_right_path ="resources/imgs/bottom_right.png"

				small_logo_right_path ="resources/imgs/small_logo.png"

				surerewads_path ="resources/imgs/surerewards.png"

				analytics_path ="resources/imgs/AA_Logo.png"





				# Creating an Presentation object
				ppt = Presentation() 

				# set width and height to 16 and 9 inches.
				ppt.slide_width = Inches(16)
				ppt.slide_height = Inches(9)
				
				# Selecting blank slide
				blank_slide_layout = ppt.slide_layouts[6]


				################### First Slide #####################

				slide_one =st.empty()
				with slide_one:
				
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)


					left = Inches(1.409) 
					height = Inches(1) 
					top=Inches(2.291)

					pic = slide.shapes.add_picture(ppc_Logo_path, left,top,width=None, height=None)


					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(8.271)
					top=Inches(3.24)
					height = Inches(1.1969) 
					width = Inches(4.0118)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "PPC130 "
					p.font.bold = True
					p.font.size = Pt(65)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					################## Second Text     ###############################
					# For adjusting the Margins in inches
					
					left= Inches(7.531)
					top=Inches(4.583)
					height = Inches(0.6063) 
					width = Inches(6.083)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame
					#tf.text = "This is text inside a textbox"

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "Surerewards Insights Report"
					p.font.bold = True
					p.font.size = Pt(30)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'



					################## Third Text Text     ###############################
					# For adjusting the Margins in inches
					
					left= Inches(8.437)
					top=Inches(5.1)
					height = Inches(0.7063) 
					width = Inches(3.681)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame
					#tf.text = "This is text inside a textbox"

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					x_start = pd.to_datetime(start_date, format='%Y%m%d', errors='ignore')
					x_end = pd.to_datetime(end_date, format='%Y%m%d', errors='ignore')

					p.text =str(x_start.strftime("%Y-%d-%B"))+' to '+str(x_end.strftime("%Y-%d-%B"))
					p.font.bold = True
					p.font.size = Pt(30)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'


				#################### Report Outline ######################



				report_outline =st.empty()

				with report_outline :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4.94)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = "Report Outline "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					############





					left= Inches(1)
					top=Inches(2.114)
					height = Inches(0.941) 
					width = Inches(5.181)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.text = ' > Customer Registration'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Date'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Products Sales By Province'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Store Location'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Region'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Merchant'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					

					

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Customer Receipts Upload'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Customer Engagement'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > PPC130 Receipts Validation'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

				
				####################  Customer Registration ################
				
				customer_reg=st.empty()

				with customer_reg :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Customer Registration "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################




					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( num_reg['date'] , num_reg['num_of_reg'] , color="red", alpha=0.2)
					plt.plot(num_reg['date'] , num_reg['num_of_reg'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function


					ax.set_ylabel('Number Of Registration')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/cust_reg'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					cust_reg ="resources/plots/cust_reg.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(cust_reg , left, top,width,height)


					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total of '+ str(Total_num_reg)+' customers registered on the surereward'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' platform  from '+str(start_date)+" to "+str(end_date)
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


				### End of Reg ###


				#############  Number Of Bags By Date  ###############


				bags_by_=st.empty()

				with bags_by_ :
					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Sale By Date "
					p.font.bold = True
					p.font.size = Pt(40)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################

					




					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( bags_by_date['date'] , bags_by_date['Total number of bags'] , color="red", alpha=0.2)
					plt.plot(bags_by_date['date'] , bags_by_date['Total number of bags'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function





					ax.set_ylabel('Number Of Bags')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)


					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/bags_date'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					bags_date_img ="resources/plots/bags_date.png"



					pic = slide.shapes.add_picture(bags_date_img, left, top,width,height)


					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Surerewards customers bought a total of '+ str(bags_interval['Total number of bags'].sum())+' bags ' 
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' from  '+str(start_date)+ " to "+str(end_date)
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

             	


				
				############ Product Split By Location ###############

				product_prov=st.empty()
				
				with product_prov :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Performance By Province"
					p.font.bold = True
					p.font.size = Pt(32)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################

					producd_region = df_receiptdata.groupby(['province'])['ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor'].sum().reset_index()
					


					

					product = pd.DataFrame({"ppc_surebuild":list(producd_region['ppc_surebuild']),'ppc_surecem':list(producd_region['ppc_surecem']),'ppc_surecast':list(producd_region['ppc_surecast']),'ppc_suretech':list(producd_region['ppc_suretech']),'ppc_surewall':list(producd_region['ppc_surewall']),'ppc_sureroad':list(producd_region['ppc_sureroad']),'ppc_plaster':list(producd_region['ppc_plaster']),'ppc_motor':list(producd_region['ppc_motor'])}, index=producd_region['province'])



					
					fig, ax = plt.subplots()
					plt.tight_layout()
					# Plotting the pie chart for above dataframe


					ax =product.plot(kind="bar",width=1,align='edge')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.legend(loc='best')


					#for container in ax.containers:
					#	ax.bar_label(container,rotation=90, padding=5)

					

					plt.savefig('resources/plots/product_loc'+'.png',bbox_inches='tight')
					
					left= Inches(1)
					top=Inches(2)
					height = Inches(6) 
					width = Inches(10)

					product_img ="resources/plots/product_loc.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(product_img  , left, top,width,height)








					producd_region_ = df_receiptdata.groupby(['province'])['Total number of bags'].sum().reset_index()
					






					fig, ax = plt.subplots()
					plt.tight_layout()


					bars = ax.barh(list(producd_region_ ['province']) ,list(producd_region_['Total number of bags']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					
					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					plt.ylabel('Province')
					plt.xlabel('Total Number of bags')


					plt.savefig('resources/plots/'+'location_tot.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					tot_location ="resources/plots/location_tot.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(tot_location , left, top,width,height)












				#################   Performance By Store Location #############################

				store_location=st.empty()

				with store_location:


					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Sales By Store Location"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					############## Adding Merchant Performance

					#name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					#df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					#sorted_df=df.sort_values('Total number of bags', ascending=False)

					#mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					#data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					#mechant_freq_df = pd.DataFrame.from_dict(data)



					################# Top Performong Merchant By Sale Quantity
					name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					df =df_receiptdata.groupby(['city'])[name_].apply(lambda x : x.astype(int).sum())
					sorted_df=df.sort_values('Total number of bags', ascending=False)


					plot_df = sorted_df.head(20)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)


					fig, ax = plt.subplots()
					plt.tight_layout()	

					ax= plot_df.plot.barh(stacked=True)
						

					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					#for container in ax.containers:
					#	ax.bar_label(container, padding=5)




					# Label with label_type 'center' instead of the default 'edge'

					#ax.bar_label(label_type='center')

					#ax.bar_label(p2)




					ax.set_ylabel("Store Location")
					ax.set_xlabel("Number Of Bags")

					plt.savefig('resources/plots/'+'top_city.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_city_by_no ="resources/plots/top_city.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_city_by_no , left, top,width,height)


                    ############### Top city by sales  frequency
					mechant_freq_dict = unique_names(df_receiptdata['city'])
					data = {'Store Location': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					mechant_freq_df = pd.DataFrame.from_dict(data)


					plot_df =mechant_freq_df.head(20)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					bars = ax.barh(list(plot_df['Store Location']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					
					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					plt.ylabel('Store Location')
					plt.xlabel('Sales Frequency')


					plt.savefig('resources/plots/'+'top_city_by_freq.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_city_by_freq ="resources/plots/top_city_by_freq.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_city_by_freq , left, top,width,height)


					################ Adding Comment #######################

					# creating textBox
					left= Inches(1)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the left shows top 20 performing store location by product and the total number of bags'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the right shows top 20 performing store location by the number of customers who made sales'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'




			 
			 
			 
			 
			 	#############  Region Contribution ###################

			 
				region_=st.empty()

				with region_ :
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2.5)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Product Performance By Region "
					p.font.bold = True
					p.font.size = Pt(32)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					################# Addding  Plot  ################################


					
					fig, ax = plt.subplots(figsize=(10, 6))

					# Plotting the pie chart for above dataframe
					ax = df_receiptdata.groupby(['region']).sum().plot(kind='pie', y='Total number of bags', autopct='%1.0f%%')

					



					plt.savefig('resources/plots/region_perc'+'.png',bbox_inches='tight')
					
					left= Inches(1)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(4)

					region_perc_img ="resources/plots/region_perc.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(region_perc_img  , left, top,width,height)



					#######################    Adding Second  Plot ##########################


					fig, ax = plt.subplots(figsize=(10, 6))



					
					# Plotting the pie chart for above dataframe
					ax = df_receiptdata.groupby(['region']).sum().plot(kind='bar', y='Total number of bags')


					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)


					for container in ax.containers:
						ax.bar_label(container, padding=5)


					

					
					
	


					plt.savefig('resources/plots/region_sum'+'.png',bbox_inches='tight')
					
					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(4)

					region_sum_img ="resources/plots/region_sum.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(region_sum_img  , left, top,width,height)


					#######################################################################



					sum_region =df_receiptdata.groupby(['region'])['Total number of bags'].sum().reset_index()

					coastal_bags = sum_region.loc[sum_region['region'] =='coastal']['Total number of bags'].item()

					inland_bags = sum_region.loc[sum_region['region'] =='inland']['Total number of bags'].item()




					# creating textBox
					left= Inches(3)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Inland contributed   '+ str(inland_bags)+' bags , translating to '+str((inland_bags*50)/1000) +' tons of cement.'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.text = '> Coastal ranked in '+str(coastal_bags )+' bags of PPC cement translating to '+str((coastal_bags*50)/1000)+' tons of cement.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					
			 ######################################################



					#pic = slide.shapes.add_picture(chart, left,top)

                ################### Top Performing Merchant ############

				Merchant_pef=st.empty()

				with Merchant_pef:


					
					
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Top 20 Performing Merchant"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'




					############## Adding Merchant Performance

					#name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					#df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					#sorted_df=df.sort_values('Total number of bags', ascending=False)

					#mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					#data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					#mechant_freq_df = pd.DataFrame.from_dict(data)



					################# Top Performong Merchant By Sale Quantity
					name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

					df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
					sorted_df=df.sort_values('Total number of bags', ascending=False)


					plot_df = sorted_df.head(20)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)


					ax = plot_df.plot.barh(stacked=True)
					plt.tight_layout()		

					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.set_ylabel("Merchant")
					ax.set_xlabel("Number Of Bags")

					#for container in ax.containers:
					#	ax.bar_label(container, padding=5)



					plt.savefig('resources/plots/'+'top_mecharnt_by_no.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_mecharnt_by_no ="resources/plots/top_mecharnt_by_no.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_mecharnt_by_no , left, top,width,height)


                    ############### Top Mechart by sales  frequency
					mechant_freq_dict = unique_names(df_receiptdata['mechant'])
					data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
					mechant_freq_df = pd.DataFrame.from_dict(data)


					plot_df =mechant_freq_df.head(20)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					bars = ax.barh(list(plot_df['merchant']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')


					plt.ylabel('Merchant')
					plt.xlabel('Sales Frequency')


					plt.savefig('resources/plots/'+'top_mecharnt_by_freq.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(8)
					top=Inches(2)
					height = Inches(4) 
					width = Inches(7)

					top_mecharnt_by_freq ="resources/plots/top_mecharnt_by_freq.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(top_mecharnt_by_freq , left, top,width,height)


					################ Adding Comment #######################

					# creating textBox
					left= Inches(1)
					top=Inches(6)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the left shows top 20 merchant performing by product and the total number of bags'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Visual on the right shows top 20 merchant performance by the number of customers who made sales'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

                ##########  Receipts Upload  ######################


				recpt_upload=st.empty()

				with recpt_upload:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Receipt Upload"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					############ Adding Plot #################


		
					N = 3
					No_Promo = (num_receipts['no_of_receipts_upload'].sum(), num_valid_receipts["no_of_valid_receipts"].sum(), num_invalid_receipts["no_of_invalid_receipts"].sum()  )
					Promo = (num_promo_receipts['no_of_receipts_upload'].sum(), num_valid_promo_receipts["no_of_valid_receipts"].sum(),num_invalid_promo_receipts["no_of_invalid_receipts"].sum())
					
					ind = np.arange(N)    # the x locations for the groups
					width = 0.35       # the width of the bars: can also be len(x) sequence



					fig, ax = plt.subplots()
					plt.tight_layout()

					p1 = ax.bar(ind, Promo, width,  label='With PPC130')
					p2 = ax.bar(ind, No_Promo, width,bottom=Promo, label='Without PPC130')

					ax.axhline(0, color='grey', linewidth=0.8)
					ax.set_ylabel('Number Of Receipts ')
					

					ax.set_xticks(ind,labels=['Total', 'Valid', 'Invalid'])
					ax.legend()

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Label with label_type 'center' instead of the default 'edge'
					ax.bar_label(p1, label_type='center')
					ax.bar_label(p2, label_type='center')
					#ax.bar_label(p2)


					plt.savefig('resources/plots/'+'receipt_upload.png',bbox_inches='tight')
					


					left= Inches(0.5)
					top=Inches(2)
					height = Inches(5.5) 
					width = Inches(6)

					receipt_upload_path ="resources/plots/receipt_upload.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(receipt_upload_path , left, top,width,height)


					############# Adding Comments #################################333

					# creating textBox
					left= Inches(6.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total of '+ str(num_receipts['no_of_receipts_upload'].sum()+num_promo_receipts['no_of_receipts_upload'].sum())+' receipts were uploaded between '+str(start_date)+" and "+str(end_date)
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '> Out of the total receipts uploaded,'+str(num_valid_receipts["no_of_valid_receipts"].sum()+num_valid_promo_receipts["no_of_valid_receipts"].sum())+ ' were found to be valid and thus approved'
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > From the valid receipts, '+str(num_valid_receipts["no_of_valid_receipts"].sum())+' did not have PPC130 promo code'
					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > '+str( num_invalid_receipts["no_of_invalid_receipts"].sum()+num_invalid_promo_receipts["no_of_invalid_receipts"].sum())+ ' invalid receipts were uploaded, '+str(num_invalid_receipts["no_of_invalid_receipts"].sum())+' did not have PPC130 promo code.'

					p.level = 0
					#p.font.bold = True
					p.font.size = Pt(16)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'



				################### Customer Engagement #################

				customer_eng=st.empty()

				with customer_eng:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(3)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Customer Engagement"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'

					############ Adding Plot #################	

					
					fig, ax = plt.subplots()
					plt.tight_layout()

					users_ = ["New Users","Users From Campaign","Existing Users"]
				
					no_receipts = [new_u_recpt['value'].item(),camp_u_recpt['value'].item(), ex_u_recpt['value'].item()]


					# Plot horizontal bar chart

					bars = plt.barh(users_ ,no_receipts)

					# To get data labels

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
						
					# Define axes labels

					plt.xlabel("No Of Receipts ")


					plt.savefig('resources/plots/'+'user_recpt.png',bbox_inches='tight')
					

					receipt_user_path ="resources/plots/user_recpt.png"

					left= Inches(0.5)
					top=Inches(2)
					height = Inches(3) 
					width = Inches(6)
					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(receipt_user_path  , left, top,width,height)


					#### Second Visual #############

					fig, ax = plt.subplots()
					plt.tight_layout()

					users_ = ["New Users","Users From Campaign","Existing Users"]

					no_user = [new_u_numb['value'].item(),camp_u_numb['value'].item(), ex_u_numb['value'].item()]


					# Plot horizontal bar chart

					bars = plt.barh(users_ ,no_user)

					# To get data labels

					for  bar in bars:
						width = bar.get_width()
						label_y = bar.get_y() + bar.get_height() / 2
						plt.text(width, label_y, s=f'{width}')

					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
						
					# Define axes labels

					plt.xlabel("No Of Users ")


					plt.savefig('resources/plots/'+'user_no.png',bbox_inches='tight')
					

					no_user_path ="resources/plots/user_no.png"

					left= Inches(8)
					top=Inches(2)
					height = Inches(3) 
					width = Inches(6)





					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(no_user_path  , left, top,width,height)

					################## Add Comments #################

				    # creating textBox
					left= Inches(3)
					top=Inches(5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)


					total_recpt = num_receipts['no_of_receipts_upload'].sum()+num_promo_receipts['no_of_receipts_upload'].sum()
					new_u_perc =round((new_u_recpt['value'].item()/total_recpt)*100)
					ex_u_perc= round((ex_u_recpt['value'].item()/total_recpt)*100)
					camp_u_perc = round((camp_u_recpt['value'].item()/total_recpt)*100)


					p.text = ' > Out of the total '+str(total_recpt)+ ' receipts uploads, '+str(new_u_perc)+'% was from New Users ( registered between '+str(start_date)+ ' and '+ str(end_date)+' ).'

					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(camp_u_perc)+'% of receipts uploads was from Users From Campaign ( registered from the 15 February to'+str(start_date) +' ).'

					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(ex_u_perc)+'% of the receipts was from Existing Users( registered before 15 February 2022).'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > From the '+str(Total_num_reg)+' customer registration , '+str(new_u_numb['value'].item())+' customers uploaded receipts ( Customer conversion of '+str(round((new_u_numb['value'].item()/Total_num_reg)*100))+'%).'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(15)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'







				###### Receipt Validation ##########


				recpt_validation=st.empty()

				with recpt_validation:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(4)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " PPC130 Receipt Validation"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					##### placing the figure #######

					fig, ax = plt.subplots()
					plt.tight_layout()

					sizes = list(status['count'])

					# Setting labels for items in Chart
					labels = list(status['status'])

					# colors
					

					# explosion
					

					# Pie Chart
					ax =plt.pie(sizes, labels=labels,autopct='%1.1f%%', pctdistance=0.85)

					# draw circle
					centre_circle = plt.Circle((0, 0), 0.70, fc='white')
					fig = plt.gcf()

					# Adding Circle in Pie chart
					fig.gca().add_artist(centre_circle)


					plt.savefig('resources/plots/'+'status_plot.png',bbox_inches='tight')
					#st.pyplot(plt.show())


					left= Inches(0.3)
					top=Inches(2)
					height = Inches(5) 
					width = Inches(7)

					status_img ="resources/plots/status_plot.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(status_img , left, top,width,height)



					###### Adding Comments ##########################3

					apprv_ = status[status['status']=='approved']['count'].reset_index()
					limit_ = status[status['status']=='Limit reached.']['count'].reset_index()

					apprvd_per =round(((apprv_['count'][0]+limit_['count'][0])/status['count'].sum())*100)



					
					# creating textBox
					left= Inches(7.5)
					top=Inches(3)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+ str(apprvd_per )+'% of the receipts uploaded were found to be valid and thus were approved,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = 'Limit reached included'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+ str(round(100-apprvd_per))+'% of the receipts were not approved'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > The main reasons for disapproval includes, Receipt not visible , Receipt not relevant'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' Duplicate receipt and Outdated receipt.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

				######## Communication By SMS  ##############

				comm_sms=st.empty()

				with comm_sms:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

					
					left = Inches(0)
					top=Inches(0)
					height = Inches(1) 
					
					pic = slide.shapes.add_picture(top_left_path, left,top, height = height)

					left= Inches(11)
					top=Inches(0.248)
					height = Inches(1.26) 
					width = Inches(2.866)
					pic = slide.shapes.add_picture(surerewads_path, left,top,width =width,height = height)

					left= Inches(0.8)
					top=Inches(7.677)
					height = Inches(1.248) 
					width = Inches(1.299)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)





					left= Inches(12.8386)
					top=Inches(8)
					height = Inches(1) 

					pic = slide.shapes.add_picture(bottom_right_path, left,top, height = height)


					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
					


					###################### Adding text   #######################################

					# For adjusting the Margins in inches
					left= Inches(2)
					top=Inches(0.06)
					height = Inches(0.941) 
					width = Inches(5.181)
					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width, height)

					# creating textFrames
					tf = txBox.text_frame

					# adding Paragraphs
					p = tf.add_paragraph()

					# adding text
					#p.text = "This is a second paragraph that's bold and italic"

					p = tf.add_paragraph()
					p.text = " Customer Communication By SMS"
					p.font.bold = True
					p.font.size = Pt(35)
					p.font.color.rgb = RGBColor(255, 0, 0)
					p.font.name = 'Arial'


					###### Add Plots ########

					fig, ax = plt.subplots(figsize=(10, 6))


					# Same, but add a stronger line on top (edge)
					plt.fill_between( sms_numbers['date'] , sms_numbers['Number_Of_SMS_Sent'] , color="red", alpha=0.2)
					plt.plot(sms_numbers['date'] , sms_numbers['Number_Of_SMS_Sent'] , color="black", alpha=0.6)
					# See the line plot function to learn how to customize the plt.plot function


					ax.set_ylabel('Number Of SMS Sent')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					# Define the date format
					date_form = DateFormatter("%b-%d")
					ax.xaxis.set_major_formatter(date_form)



					plt.savefig('resources/plots/cust_sms'+'.png',bbox_inches='tight')
					
					left= Inches(0.5)
					top=Inches(1.5)
					height = Inches(4) 
					width = Inches(7)

					cust_sms ="resources/plots/cust_sms.png"


					#pic = slide.shapes.add_picture(top_mech_no , left,top,width =width,height = height)
					pic = slide.shapes.add_picture(cust_sms , left, top,width,height)





					#########################


					
					# creating textBox
					left= Inches(8)
					top=Inches(2)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > A total  of '+ str( sms_numbers['Number_Of_SMS_Sent'].sum() )+' SMS where sent between 15 Feb  2022 and '+ str(end_date)
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'




					total_sms_date =len(list(sms_numbers_on_date['body']))
					withdrawm_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('withdraw')]['body'].count()
					succes_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('successfully captured')]['body'].count()
					less_bag_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('Miss Out')]['body'].count()

 

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = '  > From the SMS sent ,'+str(withdrawm_no)+' was SMS about withdrawal request,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((withdrawm_no/total_sms_date)*100))+'% of the total SMS sent. '
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(succes_no )+' was SMS about successfully captured receipts,'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((succes_no/total_sms_date)*100))+'%  of the total SMS sent.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > '+str(less_bag_no)+' was SMS sent to customers who bought less than 10 bags, '
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(10)
					p.text = ' which is '+str(round((less_bag_no/total_sms_date)*100))+'%  of the total SMS sent.'
					p.level = 1
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(112, 48, 160)
					p.font.name = 'Arial'


					################ Botttom Comments ####################



					left= Inches(5) 
					top=Inches(5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' Types Of SMS'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(20)
					p.font.color.rgb = RGBColor(225, 0, 0)
					p.font.name = 'Arial'







					left= Inches(1) 
					top=Inches(5.5)
					height = Inches(1) 
					width = Inches(15)


					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 1) Request to withdraw is received and will be processed within 24 hours to the following account:'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 2) Your receipt has been successfully captured and Well Done! You have successfully been entered into our daily draw to win R 10 000 CASH'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' 3) Don’t Miss Out!. Purchase 10 bags or more, Apply Promo Code PPC130 on SUREREWARDS and STAND A CHANCE TO WIN R 10 000'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(14)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'



                ############ Last Slide  ###############
				last_slide=st.empty()

				with last_slide:
					# Attaching slide to ppt
					slide = ppt.slides.add_slide(blank_slide_layout) 
					
					# adding images

	


					left= Inches(5)
					top=Inches(0.5)
					height = Inches(6) 
					width = Inches(6)
					pic = slide.shapes.add_picture(analytics_path, left,top,width =width,height = height)






					left= Inches(3.2757)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)

					###################### Adding text   #######################################

					left= Inches(5.5)
					top=Inches(6)
					height = Inches(0.941) 
					width = Inches(5.181)

					# creating textBox
					txBox = slide.shapes.add_textbox(left, top,width =width, height = height)

					# creating textFrames
					tf = txBox.text_frame



					p = tf.add_paragraph()

					p.text = 'THANK YOU'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(60)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					 




					






                ##  Saving  to file
				#ppt.save('Daily Report.pptx')

				#f = open('Daily Report.pptx','r')


				#########   Downloading the Presentation #######

				from io import BytesIO


				# save the output into binary form
				binary_output = BytesIO()
				ppt.save(binary_output) 

				st.download_button(label = 'Download  Report',data = binary_output.getvalue(),file_name = str(start_date)+" to "+str(end_date)+'  Report.pptx')

				
		################################################################################
		################################################################################
			


			


				




		





	if selection == "Product Performance":


		df_receiptdata=pd.read_sql_query("SELECT mechant,location,action as platform_massage,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata ",conn)


		### split data into city and province
		df_receiptdata[['city','province','mixed_location']] = df_receiptdata['location'].str.split(',', expand=True)
		df_receiptdata.drop('location', axis=1, inplace=True)

		#Removing white spaces
		df_receiptdata['city'] = df_receiptdata['city'].str.strip() 
		df_receiptdata['province'] = df_receiptdata['province'].str.strip()
		df_receiptdata['mechant'] = df_receiptdata['mechant'].str.strip()

		#lowering all letters
		df_receiptdata['city'] =df_receiptdata['city'].str.lower()
		df_receiptdata['province'] = df_receiptdata['province'].str.lower()
		df_receiptdata['mechant'] = df_receiptdata['mechant'].str.lower()


		#Removing all punctuations

		df_receiptdata['city'] =df_receiptdata['city'].str.replace(r'[^\w\s]+', '', regex=True)
		df_receiptdata['province'] = df_receiptdata['province'].str.replace(r'[^\w\s]+', '', regex=True)
		df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace(r'[^\w\s]+', '', regex=True)

		
		#Removing all numbers from strings

		df_receiptdata['city'] =df_receiptdata['city'].str.replace('\d+', '', regex=True)
		df_receiptdata['province'] = df_receiptdata['province'].str.replace('\d+', '', regex=True)
		df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace('\d+', '', regex=True)






		df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_motor']

		## Taking posative Values
		df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

		df_receiptdata['ppc_motor'] = df_receiptdata['ppc_motor'].abs()

        ## Receipt data from  PPC130 Campaign
		PPC130_receiptdata = df_receiptdata [df_receiptdata['receipt_captured_date']>=pd.to_datetime("'2022-02-15'").date()]


		### Visulaising The number by bags during campaign
		campaign_bags = PPC130_receiptdata.groupby(['receipt_captured_date'])[['Total number of bags']].apply(lambda x : x.astype(int).sum())

		campaign_bags ["delta"] = (PPC130_receiptdata ['Total number of bags'].pct_change()).fillna(0)

		# Index to column
		campaign_bags= campaign_bags.reset_index(level=0)

		## Number Of Bags Visual
		st.markdown("<h4 style='text-align: center; color: black;'>The visual below shows the number of bags bought by surerewards customers.</h4>", unsafe_allow_html=True)
		st.altair_chart(line_graph(campaign_bags ,'receipt_captured_date','Total number of bags'), use_container_width=True)


		## Grouping By Weekday
		PPC130_receiptdata['receipt_upload_date'] = pd.to_datetime(PPC130_receiptdata['receipt_upload_date'], errors='coerce')
		PPC130_receiptdata['weekday'] = PPC130_receiptdata['receipt_upload_date'].dt.day_name()


		## Numbers of bags by weekday


		mean_weekday =PPC130_receiptdata.groupby(['weekday']).mean()
		sum_weekday =PPC130_receiptdata.groupby(['weekday']).sum()

		sorted_weekdays = ['Sunday','Saturday','Friday','Thursday','Wednesday','Tuesday','Monday']

		sort_mean_week_dct={}
		sort_sum_week_dct={}
		for i in sorted_weekdays:
			sort_mean_week_dct[i]=round(mean_weekday['Total number of bags'][i])
			sort_sum_week_dct[i]=round(sum_weekday['Total number of bags'][i])

		plot_week=pd.DataFrame(index=sorted_weekdays)
		plot_week['Average']=sort_mean_week_dct.values()
		plot_week['Total']=sort_sum_week_dct.values()


		
		#st.dataframe(PPC130_receiptdata)


		## Number of registration Visual
		st.markdown("<h5 style='text-align: center; color: black;'>The visual below shows the average and total number of bags bought buy surerewards customer by weekday.</h5>", unsafe_allow_html=True)
		

		fig, ax = plt.subplots(figsize=(10,5))
		plt.tight_layout()

		y = np.arange(len(sorted_weekdays))  # Label locations
		width = 0.4

		#ax.barh(y + width/2, plot_week['Average'], width, label='Average')
		ax.barh(y - width/2, plot_week['Total'], width, label='Total')

		# Format ticks
		ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

		# Create labels
		rects = ax.patches
		for rect in rects:
			
    		# Get X and Y placement of label from rect.
			x_value = rect.get_width()
			y_value = rect.get_y() + rect.get_height() / 2
			space = 5
			ha = 'left'
			if x_value < 0:
				space *= -1
				ha = 'right'
			label = '{:.0f}'.format(x_value)
			plt.annotate(label,(x_value, y_value), xytext=(space, 0),textcoords='offset points',va='center',ha=ha)

		# Set y-labels and legend
		ax.set_yticklabels(sorted_weekdays)
		ax.legend(loc='lower right')
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		# To show each y-label, not just even ones
		plt.yticks(np.arange(min(y), max(y)+1, 1.0))
		st.pyplot(fig)



		st.markdown("<h3 style='text-align: center; color: red;'>Overall Product Performance </h3>", unsafe_allow_html=True)





		container = st.container()
		col1, col2,col3 = st.columns(3)

		with container:
			with col1:
				metric("Total No of bags from Surerewards Customers", df_receiptdata['Total number of bags'].sum())	

			with col2:
				metric("Total No of bags from PPC130 Campaign Customers ", PPC130_receiptdata['Total number of bags'].sum())
			with col3:
				metric("Total No of bags before PPC130 Campaign", df_receiptdata['Total number of bags'].sum() -PPC130_receiptdata['Total number of bags'].sum())

			
		fig1, ax1 = plt.subplots()
		labels =["Before PPC130 Campaign", "PPC130 Campaign "]
		sizes = [ df_receiptdata['Total number of bags'].sum() -PPC130_receiptdata['Total number of bags'].sum(),PPC130_receiptdata['Total number of bags'].sum()]
		ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
	
		st.pyplot(fig1)


		
		st.markdown("<h3 style='text-align: center; color: red;'>PPC Product performance </h3>", unsafe_allow_html=True)


		container = st.container()
		col1, col2,col3,col4 = st.columns(4)

		with container:
			with col1:
				metric('ppc_surebuild', df_receiptdata['ppc_surebuild'].sum())	

			with col2:
				metric('ppc_surecem',df_receiptdata['ppc_surecem'].sum() )
			with col3:
				metric('ppc_surecast', df_receiptdata['ppc_surecast'].sum())

			with col4:
				metric('ppc_suretech', df_receiptdata['ppc_suretech'].sum())


		
		container = st.container()
		col1, col2,col3,col4 = st.columns(4)

		with container:
			with col1:
				metric('ppc_surewall', df_receiptdata['ppc_surewall'].sum())	

			with col2:
				metric('ppc_sureroad',df_receiptdata['ppc_sureroad'].sum())
			with col3:
				metric('ppc_plaster', df_receiptdata['ppc_plaster'].sum())

			with col4:
				metric('ppc_motor', abs(df_receiptdata['ppc_motor'].sum()))


		



	

		
		product_name = ['ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

		product_values =[df_receiptdata['ppc_surebuild'].sum(),df_receiptdata['ppc_surecem'].sum() ,df_receiptdata['ppc_surecast'].sum(),df_receiptdata['ppc_suretech'].sum(),df_receiptdata['ppc_surewall'].sum(),df_receiptdata['ppc_sureroad'].sum(),df_receiptdata['ppc_plaster'].sum(),df_receiptdata['ppc_motor'].sum()]

		df = pd.DataFrame({'PPC Products': product_name,  'Total No of Bags': product_values})
		

		plot = alt.Chart(df).mark_bar().encode(x='PPC Products', y='Total No of Bags')
		st.altair_chart(plot, use_container_width=True)


		#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

		#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)


		st.markdown("<h3 style='text-align: center; color: red;'>Merchant  performance By Number Of bags and Sales Frequency</h3>", unsafe_allow_html=True)

		top_mech=st.radio("Top Performing Merchant",("Top 10 Merchant","Top 20 Merchant"))
		### Top Performing Machants

		name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_motor']

		df =df_receiptdata.groupby(['mechant'])[name_].apply(lambda x : x.astype(int).sum())
		sorted_df=df.sort_values('Total number of bags', ascending=False)

		mechant_freq_dict = unique_names(df_receiptdata['mechant'])
		data = {'merchant': mechant_freq_dict.keys(), 'Sales Frequency': mechant_freq_dict.values()}
		mechant_freq_df = pd.DataFrame.from_dict(data)





		if top_mech =="Top 10 Merchant":




			container = st.container()
			col1, col2 = st.columns(2)

			with container:
				with col1:

					plot_df = sorted_df.head(10)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)




					ax = plot_df.plot.barh(stacked=True,figsize=(10,5))


					
			


					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.set_ylabel("Merchant")
					ax.set_xlabel("Number Of Bags")
					st.pyplot(plt.show())
	

				with col2:
	
					plot_df =mechant_freq_df.head(10)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					ax.barh(list(plot_df['merchant']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					plt.ylabel('Merchant')
					plt.xlabel('Sales Frequency')
					st.pyplot(fig)

		if top_mech =="Top 20 Merchant":




			container = st.container()
			col1, col2 = st.columns(2)

			with container:
				with col1:

					### Setting to 20

					plot_df = sorted_df.head(20)
					plot_df = plot_df.sort_values('Total number of bags', ascending=True)
					plot_df = plot_df.drop(['Total number of bags'], axis = 1)




					ax = plot_df.plot.barh(stacked=True,figsize=(10,5))
					plt.tight_layout()


					
			


					# add labels
					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)
					ax.set_ylabel("Merchant")
					ax.set_xlabel("Number Of Bags")
					st.pyplot(plt.show())
	

				with col2:

					### Setting to 20
	
					plot_df =mechant_freq_df.head(20)
					plot_df=plot_df.sort_values('Sales Frequency', ascending=True)


					fig, ax = plt.subplots()
					plt.tight_layout()


					ax.barh(list(plot_df['merchant']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

					plt.ylabel('Merchant')
					plt.xlabel('Sales Frequency')
					st.pyplot(fig)







	if selection == "Customer Location":

		#select latitude,longitude from userlocations
		df = pd.DataFrame(np.random.randn(1000, 2) / [1, 1] + [-25.99, 28.13],
		columns=['lat','lon'])
		#[-25.993138, 28.128150]
		position = pd.read_sql_query("select latitude as lat,longitude as lon from userlocations",conn)


		
		st.map(position )



		




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


		df_receiptdata=pd.read_sql_query("SELECT location,cast(createdAt as date) as date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(createdAt as date) >= '2022-02-15'" ,conn)
 
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


		df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_motor']

		## Taking posative Values
		df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

		df_receiptdata['ppc_motor'] = df_receiptdata['ppc_motor'].abs()


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
		

			








			






		

		
	
	
	# Building out the predication page
	if selection == "Surerewards Customers":
		st.markdown("<h1 style='text-align: center; color: red;'>PPC130 Surerewards Insights</h1>", unsafe_allow_html=True)


		
		
	

		# Loaading Datasets
		num_bags =pd.read_sql_query("select cast(r.updatedAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  between '2022-02-15' and current_date() group by date" ,conn)
		
		num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15' group by date ",conn)

		num_reg_ =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15'  ",conn)
		num_reg_total =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users ",conn)

		num_promo_reg = pd.read_sql_query("Select cast(createdAt as date) as date,count(*) as No_Promocode from users where code = 'PPC130'   ",conn)

		num_receipts_total=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status != 'unprocessed'  ",conn)
		num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status != 'unprocessed' and cast(receipts.updatedAt as date) >='2022-02-15' group by date ",conn)
		
		num_valid_receipts_total =pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') ",conn)
		num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)

		#num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)

		num_user_r_upload_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.')  ",conn)
		num_user_r_upload=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >= '2022-02-15' ",conn)

		num_user_valid_receipts_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed')  ",conn)
		num_user_valid_receipts=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)
		

		
		status=pd.read_sql_query("select status, count(*) as count from users as u join receipts as r on u.id = r.user_id where cast(r.createdAt as date) >='2022-04-15' and status != 'unprocessed' group by status",conn)
		
	



			
        ## Number of registration Visual
		st.markdown("<h4 style='text-align: center; color: black;'>The visual below shows the number of customer registration on the surerewards platform.</h4>", unsafe_allow_html=True)
		
		num_reg["delta"] = (num_reg["num_of_reg"].pct_change()).fillna(0)
		st.altair_chart(line_graph(num_reg ,"date","num_of_reg").interactive(), use_container_width=True)

		## Number of registration receipts upload
		st.markdown("<h4 style='text-align: center; color: black;'>The visual below shows the number of receipts upload on the surerewards platform.</h4>", unsafe_allow_html=True)
		
		num_receipts["delta"] = (num_receipts["no_of_receipts_upload"].pct_change()).fillna(0)
		st.altair_chart(line_graph(num_receipts ,"date","no_of_receipts_upload").interactive(), use_container_width=True)
       
	   
	   










		## To be Delete

		#st.bar_chart(bags_by_weekday ,use_container_width=True)

		#chart = (alt.Chart(sorted_week_bags).mark_bar().encode(alt.X("date"),alt.Y("Average_no_bags"),alt.Color("date:O"),alt.Tooltip(["date"]),).interactive())
		#st.altair_chart(chart)

		## Space 

		st.text("")
		st.text("")
		st.text("")

		## Space



		
		st.markdown("<h2 style='text-align: center; color: black;'>Key Performance Indicators ( KPIs ).</h2>", unsafe_allow_html=True)

		
		


		

		st.markdown("<h3 style='text-align: center; color: red;'>Number of  Customers</h3>", unsafe_allow_html=True)

		container = st.container()
		col1, col2,col3= st.columns(3)

		with container:
			with col1:
				metric(" Total No Of Surerewards Customers ", num_reg_total['num_of_reg'].sum())	

			with col2:
				metric(" No Of Customers from PPC130 Campaign ",num_reg_['num_of_reg'].sum())
			with col3:
				metric("Customers With PPC130 Promo Code",num_promo_reg['No_Promocode'].sum())

		st.markdown("<h3 style='text-align: center; color: red;'>Customer Receipts Upload</h3>", unsafe_allow_html=True)

		container = st.container()
		col1, col2,col3,col4= st.columns(4)

		with container:
			with col1:
				metric("Total No of Receipts Upload on Surerewards",  num_receipts_total['no_of_receipts_upload'].sum())	

			with col2:
				metric("No of Receipts Upload From PPC130 Campaign" ,num_receipts['no_of_receipts_upload'].sum())
			with col3:
				metric("Total No of Valid Receipts on Surerewards",num_valid_receipts_total["no_of_valid_receipts"].sum())

			with col4:
				metric("No of Valid Receipts From PPC130 Campaign",num_valid_receipts["no_of_valid_receipts"].sum())


		num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >='2022-02-15'  ",conn)
		num_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >='2022-02-15' ",conn)

		num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code != 'PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)
		num_valid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)

		num_invalid_promo_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code  ='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)
		num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)
		
		
		N = 3
		No_Promo = (num_receipts['no_of_receipts_upload'].sum(), num_valid_receipts["no_of_valid_receipts"].sum(), num_invalid_receipts["no_of_invalid_receipts"].sum()  )
		Promo = (num_promo_receipts['no_of_receipts_upload'].sum(), num_valid_promo_receipts["no_of_valid_receipts"].sum(),num_invalid_promo_receipts["no_of_invalid_receipts"].sum())
		menStd = (2, 3, 4, 1, 2)
		womenStd = (3, 5, 2, 3, 3)
		ind = np.arange(N)    # the x locations for the groups
		width = 0.35       # the width of the bars: can also be len(x) sequence



		fig, ax = plt.subplots()
		plt.tight_layout()

		p1 = ax.bar(ind, Promo, width,  label='With PPC130')
		p2 = ax.bar(ind, No_Promo, width,bottom=Promo, label='Without PPC130')

		ax.axhline(0, color='grey', linewidth=0.8)
		ax.set_ylabel('Number Of Receipts ')
		ax.set_title('PPC130 Receipt Upload')
		ax.spines['right'].set_visible(False)
		ax.spines['top'].set_visible(False)
		ax.set_xticks(ind,labels=['Total', 'Valid', 'Invalid'])
		ax.legend()

		# Label with label_type 'center' instead of the default 'edge'
		ax.bar_label(p1, label_type='center')
		ax.bar_label(p2, label_type='center')
		#ax.bar_label(p2)

		st.pyplot(fig)



	
		st.markdown("<h3 style='text-align: center; color: red;'>Customer Engagement</h3>", unsafe_allow_html=True)

		container = st.container()
		col1, col2,col3,col4= st.columns(4)

		with container:
			with col1:
				metric("Total No of Surerewards Customers With Recipets Upload",  num_user_r_upload_total['no_of_receipts_upload'].sum())	

			with col2:
				metric("PPC130 Campaign  Customers With Recipets Upload" ,num_user_r_upload['no_of_receipts_upload'].sum())
			with col3:
				metric("Total Surerewards Customers With Valid Recipets",num_user_valid_receipts_total["no_of_users_valid_receipts"].sum())

			with col4:
				metric("PPC130 Campaign Customers With Valid Recipets ",num_user_valid_receipts["no_of_users_valid_receipts"].sum())


		
		
		
		
		
		st.markdown("<h3 style='text-align: center; color: red;'>Customer Conversion By Receipt Upload</h3>", unsafe_allow_html=True)

		container = st.container()
		col1, col2= st.columns(2)

		with container:
			with col1:
				metric("Overall Conversion rate",   "{0:.0%}".format(num_user_r_upload_total['no_of_receipts_upload'].sum()/num_reg_total['num_of_reg'].sum()) )

			with col2:
				metric("PPC130 Campaign Conversion rate" , "{0:.0%}".format(num_user_r_upload['no_of_receipts_upload'].sum()/num_reg['num_of_reg'].sum()))



		#chart = alt.Chart(status).mark_arc(innerRadius=50).encode(theta=alt.Theta(field="count", type="quantitative"), color=alt.Color(field="status", type="nominal"),)
		#st.altair_chart(chart, use_container_width=True)

		# Setting size in Chart based on
		# given values

		st.markdown("<h3 style='text-align: center; color: red;'>PPC130 Receipt Validation</h3>", unsafe_allow_html=True)

				
		fig, ax = plt.subplots()
		plt.tight_layout()

		sizes = list(status['count'])

		# Setting labels for items in Chart
		labels = list(status['status'])


		# Pie Chart
		ax =plt.pie(sizes, labels=labels,autopct='%1.1f%%', pctdistance=0.85)

		# draw circle
		centre_circle = plt.Circle((0, 0), 0.70, fc='white')
		fig = plt.gcf()

		# Adding Circle in Pie chart
		fig.gca().add_artist(centre_circle)

		st.pyplot(fig)



		



				

				
			

			


		
		#def metric_row(data):
		#	#for i, (label, value) in enumerate(data.items()):
		#	#	with columns[i]:
		#	#		components.html(_build_metric(label, value))

		#def metric(label, value):
		#	components.html(_build_metric(label, value))










# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
