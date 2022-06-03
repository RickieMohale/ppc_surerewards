



df_receiptdata=pd.read_sql_query("SELECT mechant,location,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor as ppc_mortar FROM receiptdata ",conn)


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






df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_mortar']

## Taking posative Values
df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]

df_receiptdata['ppc_mortar'] = df_receiptdata['ppc_mortar'].abs()

## Receipt data from  PPC130 Campaign
PPC130_receiptdata = df_receiptdata [df_receiptdata['receipt_captured_date']>=pd.to_datetime("'2022-02-15'").date()]


### Visulaising The number by bags during campaign
campaign_bags = PPC130_receiptdata.groupby(['receipt_captured_date'])[['Total number of bags']].apply(lambda x : x.astype(int).sum())

campaign_bags ["delta"] = (PPC130_receiptdata ['Total number of bags'].pct_change()).fillna(0)

# Index to column
campaign_bags = campaign_bags.reset_index(level=0)




## Number Of Bags Visual
st.markdown("<h4 style='text-align: center; color: black;'>The visual below shows the number of bags bought by surerewards customers.</h4>", unsafe_allow_html=True)




##################### Number Of Bags ########################################
bags_by_date= pd.read_sql_query("select cast(createdAt as date) as date,sum(ppc_surebuild) as ppc_surebuild,sum(ppc_surecem) as ppc_surecem,sum(ppc_surecast) as ppc_surecast,sum(ppc_suretech) as ppc_suretech,sum(ppc_surewall) as ppc_surewall,sum(ppc_sureroad) as ppc_sureroad,sum(ppc_plaster) as ppc_plaster, sum(ppc_motor) as ppc_mortar FROM receiptdata group by date",conn)
bags_by_date['Total number of bags']=bags_by_date['ppc_surebuild']+bags_by_date['ppc_surecem'] +bags_by_date['ppc_surecast']+bags_by_date['ppc_suretech']+bags_by_date['ppc_surewall']+bags_by_date['ppc_sureroad']+bags_by_date['ppc_plaster']+bags_by_date['ppc_mortar']

########################## Reciepts Upload ########################################

dates =[str(x) for x in bags_by_date['date'].tolist()]

no_bags_chart = {"title": {"text": 'Total Number Of Bags',"left": 'center'},"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' }}},
"tooltip": {"trigger": 'axis',"axisPointer": {"type": 'cross',"label": {"backgroundColor": '#6a7985'}}},
"grid": {"left": '3%',"right": '4%',"bottom": '20%',"containLabel":"true" },"dataZoom": [{"show": "true","realtime": "true",
"start": 90,"end": 100},{"type": 'inside',"realtime": "true","start": 65,"end": 100}],"xAxis": [{"type": 'category',"boundaryGap": "false","data": dates}],"yAxis": [{"type": 'value'}],
"series": [{"name":'No Of Receipts',"type": 'line',"stack": 'Total',"areaStyle": {},"emphasis": {"focus": 'series'},
"data": bags_by_date['Total number of bags'].tolist()}]}




product_split = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
"restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
"roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(bags_by_date['ppc_surewall'].sum()), "name": 'Surewall'},{ "value":int(bags_by_date['ppc_surecem'].sum()), "name": 'Surecem'},{ "value":int(bags_by_date['ppc_sureroad'].sum()), "name": 'Sureroad'},{ "value": int(bags_by_date['ppc_surebuild'].sum()), "name": 'Surebuild' },
{ "value":int(bags_by_date['ppc_surecast'].sum()), "name": 'Surecast'},{ "value":int(bags_by_date['ppc_suretech'].sum()), "name": 'Suretech'},
{ "value":int(bags_by_date['ppc_plaster'].sum()), "name": 'Sureplaster'},{ "value":int(bags_by_date['ppc_mortar'].sum()), "name": 'Suremortar'}]}]}



col1, col2 = st.columns((1,1))
with col1:
    st_echarts(no_bags_chart , width="100%", key=1) 
      
with col2:
    st_echarts(product_split , width="100%", key=2) 


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





## Grouping By Weekday
bags_by_date['date'] = pd.to_datetime(bags_by_date['date'], errors='coerce')
bags_by_date['weekday'] = bags_by_date['date'].dt.day_name()


## Numbers of bags by weekday


mean_weekday = bags_by_date.groupby(['weekday']).mean()
sum_weekday = bags_by_date.groupby(['weekday']).sum()


st.dataframe(sum_weekday)







st.markdown("<h3 style='text-align: center; color: red;'>Overall Product Performance </h3>", unsafe_allow_html=True)



##################################################



###### The numer 8 is for -4 that was captured.



#########################################





container = st.container()
col1, col2,col3 = st.columns(3)

with container:
    with col1:
        metric("Total No of bags from Surerewards Customers", df_receiptdata['Total number of bags'].sum()+8)	

    with col2:
        metric("Total No of bags from PPC130 Campaign Customers ", PPC130_receiptdata['Total number of bags'].sum())
    with col3:
        metric("Total No of bags before PPC130 Campaign", df_receiptdata['Total number of bags'].sum() -PPC130_receiptdata['Total number of bags'].sum())

    








#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)

#st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)


st.markdown("<h3 style='text-align: center; color: red;'>Merchant  performance By Number Of bags and Sales Frequency</h3>", unsafe_allow_html=True)

top_mech=st.radio("Top Performing Merchant",("Top 10 Merchant","Top 20 Merchant"))
### Top Performing Machants

name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_mortar']

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


st.markdown("<h3 style='text-align: center; color: red;'>Product Performance By Store Location</h3>", unsafe_allow_html=True)


name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_mortar']

df =df_receiptdata.groupby(['city'])[name_].apply(lambda x : x.astype(int).sum())
sorted_df=df.sort_values('Total number of bags', ascending=False)





############### Top city by sales  frequency
location_freq_dict = unique_names(df_receiptdata['city'])
data = {'Store Location': location_freq_dict.keys(), 'Sales Frequency': location_freq_dict.values()}
location_freq_dict = pd.DataFrame.from_dict(data)



top_store_location=st.radio("Top Performing Store Location",("Top 10 Store Locations","Top 20 Store Locations"))



if top_store_location == "Top 10 Store Locations":
    
    
    container = st.container()
    col1, col2 = st.columns(2)

    with container:
        with col1:
            plot_df = sorted_df.head(10)
            plot_df = plot_df.sort_values('Total number of bags', ascending=True)
            plot_df = plot_df.drop(['Total number of bags'], axis = 1)


            fig, ax = plt.subplots()
            plt.tight_layout()	

            ax= plot_df.plot.barh(stacked=True)
                

            # add labels
            ax.legend(loc='lower right')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)


            ax.set_ylabel("Store Location")
            ax.set_xlabel("Number Of Bags")
            st.pyplot(plt.show())


        with col2:

            plot_df_location_freq =location_freq_dict .head(10)
            plot_df_location_freq=plot_df_location_freq.sort_values('Sales Frequency', ascending=True)


            fig, ax = plt.subplots()
            plt.tight_layout()


            bars = ax.barh(list(plot_df_location_freq['Store Location']) ,list(plot_df_location_freq['Sales Frequency']))

            ax.legend(loc='lower right')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            for  bar in bars:
                width = bar.get_width()
                label_y = bar.get_y() + bar.get_height() / 2
                plt.text(width, label_y, s=f'{width}')

            plt.ylabel('Store Location')
            plt.xlabel('Sales Frequency')

            st.pyplot(fig)




if top_store_location == "Top 20 Store Locations":
    
    
    container = st.container()
    col1, col2 = st.columns(2)

    with container:
        with col1:
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


            ax.set_ylabel("Store Location")
            ax.set_xlabel("Number Of Bags")
            st.pyplot(plt.show())


        with col2:

            plot_df_location_freq =location_freq_dict .head(20)
            plot_df_location_freq=plot_df_location_freq.sort_values('Sales Frequency', ascending=True)


            fig, ax = plt.subplots()
            plt.tight_layout()


            bars = ax.barh(list(plot_df_location_freq['Store Location']) ,list(plot_df_location_freq['Sales Frequency']))

            ax.legend(loc='lower right')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            for  bar in bars:
                width = bar.get_width()
                label_y = bar.get_y() + bar.get_height() / 2
                plt.text(width, label_y, s=f'{width}')

            plt.ylabel('Store Location')
            plt.xlabel('Sales Frequency')

            st.pyplot(fig)




##################### Cleaning wrong capture province   ###################################

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








############### Top city by sales  frequency
province_freq_dict = unique_names(df_receiptdata['province'])
data = {'province':province_freq_dict.keys(), 'Sales Frequency': province_freq_dict.values()}
province_freq_dict = pd.DataFrame.from_dict(data)



df =df_receiptdata.groupby(['province'])[name_].apply(lambda x : x.astype(int).sum())
sorted_df=df.sort_values('Total number of bags', ascending=False)




    


######################################################### Province Visual  ##################################################################################




st.markdown("<h3 style='text-align: center; color: red;'>Product Performance By Province</h3>", unsafe_allow_html=True)

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

product_select =st.radio("Select Product",('Total number of bags','Surebuild', 'Surecast', 'Surecem','Suretech','Surewall','Sureroad','Sureplaster','Suremortar'))

if product_select == 'Total number of bags':

    
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Total number of bags',"type": 'bar',"data": [ int(sorted_df['Total number of bags'][0]),int(sorted_df['Total number of bags'][1]),int(sorted_df['Total number of bags'][2]),int(sorted_df['Total number of bags'][3]),int(sorted_df['Total number of bags'][4]),int(sorted_df['Total number of bags'][5]),int(sorted_df['Total number of bags'][6]),int(sorted_df['Total number of bags'][7]),int(sorted_df['Total number of bags'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['Total number of bags'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['Total number of bags'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['Total number of bags'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['Total number of bags'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['Total number of bags'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['Total number of bags'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['Total number of bags'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['Total number of bags'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['Total number of bags'][8]), "name": sorted_df.index[8]}]}]}


elif product_select == 'Surebuild':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Surebuild',"type": 'bar',"data": [ int(sorted_df['ppc_surebuild'][0]),int(sorted_df['ppc_surebuild'][1]),int(sorted_df['ppc_surebuild'][2]),int(sorted_df['ppc_surebuild'][3]),int(sorted_df['ppc_surebuild'][4]),int(sorted_df['ppc_surebuild'][5]),int(sorted_df['ppc_surebuild'][6]),int(sorted_df['ppc_surebuild'][7]),int(sorted_df['ppc_surebuild'][8])]},]}
   
    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_surebuild'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_surebuild'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_surebuild'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_surebuild'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_surebuild'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_surebuild'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_surebuild'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_surebuild'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_surebuild'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Surecem':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Surecem',"type": 'bar',"data": [ int(sorted_df['ppc_surecem'][0]),int(sorted_df['ppc_surecem'][1]),int(sorted_df['ppc_surecem'][2]),int(sorted_df['ppc_surecem'][3]),int(sorted_df['ppc_surecem'][4]),int(sorted_df['ppc_surecem'][5]),int(sorted_df['ppc_surecem'][6]),int(sorted_df['ppc_surecem'][7]),int(sorted_df['ppc_surecem'][8])]},]}


    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_surecem'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_surecem'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_surecem'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_surecem'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_surecem'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_surecem'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_surecem'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_surecem'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_surecem'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Suretech':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Suretech',"type": 'bar',"data": [ int(sorted_df['ppc_suretech'][0]),int(sorted_df['ppc_suretech'][1]),int(sorted_df['ppc_suretech'][2]),int(sorted_df['ppc_suretech'][3]),int(sorted_df['ppc_suretech'][4]),int(sorted_df['ppc_suretech'][5]),int(sorted_df['ppc_suretech'][6]),int(sorted_df['ppc_suretech'][7]),int(sorted_df['ppc_suretech'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_suretech'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_suretech'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_suretech'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_suretech'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_suretech'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_suretech'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_suretech'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_suretech'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_suretech'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Surecast':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Surecast',"type": 'bar',"data": [ int(sorted_df['ppc_surecast'][0]),int(sorted_df['ppc_surecast'][1]),int(sorted_df['ppc_surecast'][2]),int(sorted_df['ppc_surecast'][3]),int(sorted_df['ppc_surecast'][4]),int(sorted_df['ppc_surecast'][5]),int(sorted_df['ppc_surecast'][6]),int(sorted_df['ppc_surecast'][7]),int(sorted_df['ppc_surecast'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_surecast'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_surecast'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_surecast'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_surecast'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_surecast'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_surecast'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_surecast'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_surecast'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_surecast'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Surewall':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Surewall',"type": 'bar',"data": [ int(sorted_df['ppc_surewall'][0]),int(sorted_df['ppc_surewall'][1]),int(sorted_df['ppc_surewall'][2]),int(sorted_df['ppc_surewall'][3]),int(sorted_df['ppc_surewall'][4]),int(sorted_df['ppc_surewall'][5]),int(sorted_df['ppc_surewall'][6]),int(sorted_df['ppc_surewall'][7]),int(sorted_df['ppc_surewall'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_surewall'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_surewall'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_surewall'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_surewall'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_surewall'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_surewall'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_surewall'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_surewall'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_surewall'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Sureroad':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Sureroad',"type": 'bar',"data": [ int(sorted_df['ppc_sureroad'][0]),int(sorted_df['ppc_sureroad'][1]),int(sorted_df['ppc_sureroad'][2]),int(sorted_df['ppc_sureroad'][3]),int(sorted_df['ppc_sureroad'][4]),int(sorted_df['ppc_sureroad'][5]),int(sorted_df['ppc_sureroad'][6]),int(sorted_df['ppc_sureroad'][7]),int(sorted_df['ppc_sureroad'][8])]},]}
    
    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_sureroad'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_sureroad'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_sureroad'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_sureroad'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_sureroad'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_sureroad'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_sureroad'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_sureroad'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_sureroad'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Sureplaster':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Sureplaster',"type": 'bar',"data": [ int(sorted_df['ppc_plaster'][0]),int(sorted_df['ppc_plaster'][1]),int(sorted_df['ppc_plaster'][2]),int(sorted_df['ppc_plaster'][3]),int(sorted_df['ppc_plaster'][4]),int(sorted_df['ppc_plaster'][5]),int(sorted_df['ppc_plaster'][6]),int(sorted_df['ppc_plaster'][7]),int(sorted_df['ppc_plaster'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_mortar'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_plaster'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_plaster'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_plaster'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_plaster'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_plaster'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_plaster'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_plaster'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_plaster'][8]), "name": sorted_df.index[8]}]}]}

elif product_select == 'Suremortar':
    province_bar = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
    "yAxis": {"type": 'category',"data": [sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
    "series": [{"name": 'Suremortar',"type": 'bar',"data": [ int(sorted_df['ppc_mortar'][0]),int(sorted_df['ppc_mortar'][1]),int(sorted_df['ppc_mortar'][2]),int(sorted_df['ppc_mortar'][3]),int(sorted_df['ppc_mortar'][4]),int(sorted_df['ppc_mortar'][5]),int(sorted_df['ppc_mortar'][6]),int(sorted_df['ppc_mortar'][7]),int(sorted_df['ppc_mortar'][8])]},]}

    province_pie = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
    "restore": { "show": "true" }}}, "series": [ { "name": 'Product', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
    "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(sorted_df['ppc_mortar'][0]), "name": sorted_df.index[0]},
    { "value":int(sorted_df['ppc_mortar'][1]), "name": sorted_df.index[1]},{ "value":int(sorted_df['ppc_mortar'][2]), "name": sorted_df.index[2]},{ "value":int(sorted_df['ppc_mortar'][3]), "name": sorted_df.index[3]},
    { "value":int(sorted_df['ppc_mortar'][4]), "name": sorted_df.index[4]},{"value":int(sorted_df['ppc_mortar'][5]), "name": sorted_df.index[5]},{"value":int(sorted_df['ppc_mortar'][6]), "name": sorted_df.index[6]},
    {"value":int(sorted_df['ppc_mortar'][7]), "name": sorted_df.index[7]},{"value":int(sorted_df['ppc_mortar'][8]), "name": sorted_df.index[8]}]}]}



container = st.container()
col1, col2= st.columns((1,1))

with container:
    with col1:
        st_echarts(options=province_bar, width="100%", key=18) 

  
    with col2:
        st_echarts(options=province_pie, width="100%", key=19) 




st.markdown("<h3 style='text-align: center; color: red;'>Product Performance By Province's Sales Frequency </h3>", unsafe_allow_html=True)


province_bar_ = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"dataZoom": [{"show": "true","realtime": "true",
"start": 90,"end": 100},{"type": 'inside',"realtime": "true","start": 65,"end": 100}],"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
"yAxis": {"type": 'category',"data": [province_freq_dict['province'][0],province_freq_dict['province'][1],province_freq_dict['province'][2],province_freq_dict['province'][3],province_freq_dict['province'][4],province_freq_dict['province'][5],province_freq_dict['province'][6],province_freq_dict['province'][7],province_freq_dict['province'][8]]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
"series": [{"type": 'bar',"data": [int(province_freq_dict['Sales Frequency'][0]),int(province_freq_dict['Sales Frequency'][1]),int(province_freq_dict['Sales Frequency'][2]),int(province_freq_dict['Sales Frequency'][3]),int(province_freq_dict['Sales Frequency'][4]),int(province_freq_dict['Sales Frequency'][5]),int(province_freq_dict['Sales Frequency'][6]),int(province_freq_dict['Sales Frequency'][7]),int(province_freq_dict['Sales Frequency'][8])]}]}

st_echarts(options=province_bar_, width="100%", key=181) 




province_bar_ = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
"yAxis": {"type": 'category',"data": [province_freq_dict['province'][0],province_freq_dict['province'][1],province_freq_dict['province'][2],province_freq_dict['province'][3],province_freq_dict['province'][4],province_freq_dict['province'][5],province_freq_dict['province'][6],province_freq_dict['province'][7],province_freq_dict['province'][8]]},"label": {"show": "true","position": 'right',"valueAnimation": "true"},
"series": [{"type": 'bar',"data": [int(province_freq_dict['Sales Frequency'][0]),int(province_freq_dict['Sales Frequency'][1]),int(province_freq_dict['Sales Frequency'][2]),int(province_freq_dict['Sales Frequency'][3]),int(province_freq_dict['Sales Frequency'][4]),int(province_freq_dict['Sales Frequency'][5]),int(province_freq_dict['Sales Frequency'][6]),int(province_freq_dict['Sales Frequency'][7]),int(province_freq_dict['Sales Frequency'][8])]}]}





###################################################################################################################################################################################################################################################################

#[sorted_df.index[0], sorted_df.index[1], sorted_df.index[2],sorted_df.index[3],sorted_df.index[4],sorted_df.index[5],sorted_df.index[6],sorted_df.index[7],sorted_df.index[8] ]
#[ int(sorted_df['ppc_mortar'][0]),int(sorted_df['ppc_mortar'][1]),int(sorted_df['ppc_mortar'][2]),int(sorted_df['ppc_mortar'][3]),int(sorted_df['ppc_mortar'][4]),int(sorted_df['ppc_mortar'][5]),int(sorted_df['ppc_mortar'][6]),int(sorted_df['ppc_mortar'][7]),int(sorted_df['ppc_mortar'][8])]



province_pie_ = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
"restore": { "show": "true" }}}, "series": [ { "name": 'Sales Frequency', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
"roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(province_freq_dict['Sales Frequency'][0]), "name": province_freq_dict['province'][0]},
{ "value":int(province_freq_dict['Sales Frequency'][1]), "name": province_freq_dict['province'][1]},{ "value":int(province_freq_dict['Sales Frequency'][2]), "name": province_freq_dict['province'][2]},
{ "value":int(province_freq_dict['Sales Frequency'][3]), "name": province_freq_dict['province'][3]},{ "value":int(province_freq_dict['Sales Frequency'][4]), "name": province_freq_dict['province'][4]},
{ "value":int(province_freq_dict['Sales Frequency'][5]), "name": province_freq_dict['province'][5]},{ "value":int(province_freq_dict['Sales Frequency'][6]), "name": province_freq_dict['province'][6]},
{ "value":int(province_freq_dict['Sales Frequency'][7]), "name": province_freq_dict['province'][7]},{ "value":int(province_freq_dict['Sales Frequency'][8]), "name": province_freq_dict['province'][8]},]}]}



container = st.container()
col1, col2= st.columns((1,1))

with container:
    with col1:
        st_echarts(options=province_bar_, width="100%", key=118) 

  
    with col2:
        st_echarts(options=province_pie_, width="100%", key=119) 



st.markdown("<h3 style='text-align: center; color: red;'>Product Performance By Region </h3>", unsafe_allow_html=True)


region_sum = df_receiptdata.groupby(['region']).sum()

region_sum.index[0]   
region_count = df_receiptdata["region"].value_counts()


region_sum_chart= {"title": {"text": 'Region ',"left": 'center'},"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
"restore": { "show": "true" }}}, "series": [ { "name": 'Number Of Bags', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
"roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(region_sum['Total number of bags'][0]), "name":region_sum.index[0]},{ "value":int(region_sum['Total number of bags'][1]), "name":region_sum.index[1]}]}]}






   

region_chart= {"title": {"text": 'Total Number Of Bags',"left": 'center'},"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
"restore": { "show": "true" }}}, "series": [ { "name": 'Sales Frequency', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
"roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":int(region_count[0]), "name":region_count.index[0]},{ "value":int(region_count[1]), "name":region_count.index[1]}]}]}








container = st.container()
col1, col2= st.columns((1,1))

with container:
    with col1:
        st_echarts(options=region_sum_chart, width="100%", key=120) 

  
    with col2:
        st_echarts(options=region_chart, width="100%", key=121) 











