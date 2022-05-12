



df_receiptdata=pd.read_sql_query("SELECT mechant,location,action as platform_massage,cast(createdAt as date) as receipt_upload_date,cast(updatedAt as date) as receipt_captured_date,ppc_surebuild,ppc_surecem,ppc_surecast,ppc_suretech,ppc_surewall,ppc_sureroad,ppc_plaster, ppc_motor as ppc_mortar FROM receiptdata ",conn)


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
        metric('ppc_mortar', abs(df_receiptdata['ppc_mortar'].sum()))









product_name = ['ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_mortar']

product_values =[df_receiptdata['ppc_surebuild'].sum(),df_receiptdata['ppc_surecem'].sum() ,df_receiptdata['ppc_surecast'].sum(),df_receiptdata['ppc_suretech'].sum(),df_receiptdata['ppc_surewall'].sum(),df_receiptdata['ppc_sureroad'].sum(),df_receiptdata['ppc_plaster'].sum(),df_receiptdata['ppc_mortar'].sum()]

df = pd.DataFrame({'PPC Products': product_name,  'Total No of Bags': product_values})


plot = alt.Chart(df).mark_bar().encode(x='PPC Products', y='Total No of Bags')
st.altair_chart(plot, use_container_width=True)


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




















