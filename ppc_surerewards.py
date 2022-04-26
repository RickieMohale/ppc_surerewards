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




	#st.subheader("Climate change tweet classification")

	# Creating sidebar with selection box -
	# you can create multiple pages this way
	
	options = ["Surerewards Customers","Prediction Page","Product Performance","Customer Location","Auto Reports"]
	#

	selection = st.sidebar.radio("Select Page:",options)
	#selection = st.sidebar.selectbox("Select Page", options)

	if selection == "Auto Reports":

		st.info("This Page is for generating PPC130 reports.Time Frame Reports can be for weekly or weekend report")

		report_type=st.radio("Select Report Type",("Daily Report","Time Frame Report"))

		

		if report_type == "Daily Report":

			selected_date = st.date_input("Select Report Date")
			st.write('Your Selected Date is:',selected_date)



			num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) between '2022-02-15' and '"+ str(selected_date)+"' group by date order by date",conn)
					
			num_reg['date'] =  pd.to_datetime(num_reg['date'])




			df_receiptdata=pd.read_sql_query("SELECT mechant,location,action as platform_massage,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor FROM receiptdata where cast(updatedAt as date) = '"+ str(selected_date)+"'" ,conn)



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
					p.text = ' > Product Sales By Merchant'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'
					

					
					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Product Sales By Location'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'


					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Products Sales Performance'
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
					p.text = ' > Product Sales By Region'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Customer Receipts Upload'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Customer Engagement'
					p.level = 0
					p.font.bold = True
					p.font.size = Pt(24)
					p.font.color.rgb = RGBColor(0, 0, 0)
					p.font.name = 'Arial'

					p = tf.add_paragraph()
					p.line_spacing = Pt(40)
					p.text = ' > Receipts Validation'
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

					chart = alt.Chart(num_reg).mark_area(line={'color':'darkgreen'},color=alt.Gradient(gradient='linear',stops=[alt.GradientStop(color='white', offset=0),alt.GradientStop(color='darkgreen', offset=1)],x1=1,x2=1,y1=1,y2=0)).encode(x = 'date',y = 'num_of_reg')
					
					#from altair_saver import save
					#chart.save('chart.png')
					#save(chart, "chart.png")



					left= Inches(10)
					top=Inches(8.4724)
					height = Inches(0.4173) 
					width = Inches(8.5079)


					#pic = slide.shapes.add_picture(chart, left,top)

                ################### Top Performing Merchant

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


					ax.barh(list(plot_df['merchant']) ,list(plot_df['Sales Frequency']))

					ax.legend(loc='lower right')
					ax.spines['right'].set_visible(False)
					ax.spines['top'].set_visible(False)

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





					





				#ppt.save("pptx-to-pdf-selected-slides.pdf",slides.export.SaveFormat.PDF)

				#file =ppt.save('test_4.pptx')



				#st.download_button('Download binary file', ppt)






				############# Addding Content  #######################3





				#slides = ppt.slides[0]
				#for slide in slides:
					


				#	left= Inches(0)
				#	top=Inches(8.4724)
				#	height = Inches(0.4173) 
				#	width = Inches(8.5079)


				#	pic = slide.shapes.add_picture(small_logo_right_path, left,top,width =width,height = height)
				





				# save file
				ppt.save('test_4.pptx')




		





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
		PPC130_receiptdata = df_receiptdata [df_receiptdata['receipt_upload_date']>=pd.to_datetime("'2022-02-15'").date()]


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
	if selection == "Prediction Page":

		
		
		st.markdown("<h3 style='text-align: center; color: black;'>This Page focuses on predicting number of bag and setting dynamic daily targets</h3>", unsafe_allow_html=True)




		num_bags =pd.read_sql_query("select cast(r.updatedAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  between '2022-02-15' and current_date() group by date" ,conn)
		
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
		if st.checkbox('Show How the works'):
		
			st.info("The model trained is LSTM ( Long Short Term Memory) model,which falls under Recurrent Neural Network models. This model is a Time Series Model that uses historical data for forecasting/ predicting the number of bags in the upcoming 7 days")			
		
		if st.button("Train Model"):

			train = df2.iloc[:len(df2)]
			test = df2.iloc[len(df2)-7:]


			## Scaling the Data
			from sklearn.preprocessing import MinMaxScaler
			scaler = MinMaxScaler()

			scaler.fit(train)
			scaled_train = scaler.transform(train)
			scaled_test = scaler.transform(test)

			#Pre processing
			from keras.preprocessing.sequence import TimeseriesGenerator

			# spliting into 7 days splits
			n_input = 7
			n_features = 1
			generator = TimeseriesGenerator(scaled_train, scaled_train, length=n_input, batch_size=1)


			from keras.models import Sequential
			from keras.layers import Dense
			from keras.layers import LSTM

			# define model
			model = Sequential()
			model.add(LSTM(100, activation='relu', input_shape=(n_input, n_features)))
			model.add(Dense(1))
			model.compile(optimizer='adam', loss='mse')


			# fit model
			model.fit(generator,epochs=50)

			st.markdown("<h5 style='text-align: center; color: black;'>Model Convergence</h5>", unsafe_allow_html=True)
			fig, ax = plt.subplots(figsize=(10,5))
			plt.tight_layout()
			loss_per_epoch = model.history.history['loss']
			ax=plt.plot(range(len(loss_per_epoch)),loss_per_epoch)
			plt.xlabel('Number of iterations')
			plt.ylabel('means squeared error')
			st.pyplot(fig)


			#making predictions
			test_predictions = []

			first_eval_batch = scaled_train[-n_input:]
			current_batch = first_eval_batch.reshape((1, n_input, n_features))


			test_predictions = []

			first_eval_batch = scaled_train[-n_input:]
			current_batch = first_eval_batch.reshape((1, n_input, n_features))

			for i in range(len(test)):
    
				# get the prediction value for the first batch
				current_pred = model.predict(current_batch)[0]
    
				# append the prediction into the array
				test_predictions.append(current_pred) 
    
				# use the prediction to update the batch and remove the first value
				current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)



			
			## Making Predictions
			true_predictions = scaler.inverse_transform(test_predictions)
				
			## Last day of the 
			last_day = train.index[len(list(train['number_of_bags']))-1]
			last_day=last_day.date()

			import datetime
			forward_days=[last_day+datetime.timedelta(days=1)]
			for i in range(6):    
				forward_days.append(forward_days[len(forward_days)-1]+datetime.timedelta(days=1))

			## Prediction Values
			pred_values=[]
			for i in range(len(true_predictions)):
				pred_values.append(round(true_predictions.tolist()[i][0]))

				
			## Prediction Dataframe
			content = {'date': list(pd.to_datetime(forward_days, errors='coerce')),'number_of_bags': pred_values}
			df_pred = pd.DataFrame(content).set_index('date')
			df_pred.sort_index(inplace=True)
				
			## Show dataframe prediction page
			st.markdown("<h5 style='text-align: center; color: black;'>Predicted Values </h5>", unsafe_allow_html=True)
			#st.dataframe(df_pred)

			## Insert join prediction and train dataframe
			df_pred.loc[pd.to_datetime(train.index[len(train)-1], errors='coerce')] = round(train['number_of_bags'][len(train)-1])
				
			fig, ax = plt.subplots(figsize=(10,5))
			plt.tight_layout()
			labels=['historical data','prediction']
			for i,df in enumerate([train,df_pred],1):
				df =df.sort_index()
				ax = plt.plot(df.index,df['number_of_bags'],label=labels[i-1])

			plt.legend()
			plt.xlabel('Date')
			plt.ylabel('Number Of Bags')
			plt.show()
			st.pyplot(fig)

			st.success("Success") 
			








			






		

		
	
	
	# Building out the predication page
	if selection == "Surerewards Customers":
		st.markdown("<h1 style='text-align: center; color: red;'>PPC130 Surerewards Insights</h1>", unsafe_allow_html=True)


		
		
	

		# Loaading Datasets
		num_bags =pd.read_sql_query("select cast(r.updatedAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  between '2022-02-15' and current_date() group by date" ,conn)
		
		num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15'  group by date order by date",conn)

		num_reg_ =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15'  ",conn)
		num_reg_total =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users ",conn)

		num_promo_reg = pd.read_sql_query("Select cast(createdAt as date) as date,count(*) as No_Promocode from users where code = 'PPC130'   ",conn)

		num_receipts_total=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.')   group by date",conn)
		num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >='2022-02-15' group by date ",conn)
		
		num_valid_receipts_total =pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed')  group by date",conn)
		num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)

		#num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)

		num_user_r_upload_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.')  group by date",conn)
		num_user_r_upload=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)

		num_user_valid_receipts_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed')  group by date",conn)
		num_user_valid_receipts=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  Not in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Unprocessed') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)
		#num_user_invalid_receipts=pd.read_sql_query("SELECT count(distinct(users.id))as no_of_users_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)
		
	



			
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

		
		st.markdown("<h3 style='text-align: center; color: red;'>Customer Conversion By Valid Receipt Upload</h3>", unsafe_allow_html=True)

		container = st.container()
		col1, col2= st.columns(2)

		with container:
			with col1:
				metric("Overall Conversion rate",   "{0:.0%}".format(num_user_valid_receipts_total["no_of_users_valid_receipts"].sum()/num_reg_total['num_of_reg'].sum()) )

			with col2:
				metric("PPC130 Campaign Conversion rate" , "{0:.0%}".format(num_user_valid_receipts["no_of_users_valid_receipts"].sum()/num_reg['num_of_reg'].sum()))


		



				

				
			

			


		
		#def metric_row(data):
		#	#for i, (label, value) in enumerate(data.items()):
		#	#	with columns[i]:
		#	#		components.html(_build_metric(label, value))

		#def metric(label, value):
		#	components.html(_build_metric(label, value))










# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
