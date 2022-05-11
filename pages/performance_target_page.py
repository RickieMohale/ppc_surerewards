


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
st.markdown("<h5 style='text-align: center; color: black;'>Setting Weekly Performance Targets</h5>", unsafe_allow_html=True)


st.info(" Weekly targets are based on the statistics of the number of bags sold on a daily basis.Inland and Coastal region performance  target are generated separately.")


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



###### Separating Data####


model_df =pd.DataFrame()
model_df['date']=pd.to_datetime(df_receiptdata['date'], errors='coerce')
model_df['region']  =df_receiptdata['region']
model_df['Total number of bags']  =df_receiptdata['Total number of bags']

model_df = model_df.groupby(['date','region']).agg({'Total number of bags':'sum'}).reset_index()

model_df['weekday'] = model_df['date'].dt.day_name()





inland_df =model_df[model_df['region']=='inland']

df_inland =inland_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

df_inland = df_inland .astype(int)





coastal_df =model_df[model_df['region']=='coastal']

df_coastal =coastal_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

df_coastal =df_coastal .astype(int)




if st.button( "Get Performance Target"):

    

    

    container = st.container()
    col1,col2,col3,col4,col5 = st.columns(5)

    with container:
        with col1:
            st.empty()

        with col2:
            st.markdown("<h5 style='text-align: center; color: black;'>Inland Peformance Target</h5>", unsafe_allow_html=True)
        
            st.dataframe(df_inland["Total number of bags"]["50%"])

        with col3:

            st.empty()

        with col4:
            st.markdown("<h5 style='text-align: center; color: black;'>Coastal Peformance Target</h5>", unsafe_allow_html=True)
            st.dataframe (df_coastal["Total number of bags"]["50%"])
        
        with col5:
            st.empty()
    
    st.success(" The above targets are based on the median value of number of bags sold per day.( Median is used as opposed to the mean ,due to presence of outliers in the data that skew the mean).")
        
    





if st.button( "Get Performance Statistics"):

    if st.checkbox('Show Overall Weekday Performance Statistics'):
        region_df = model_df[["weekday", 'Total number of bags']].groupby("weekday").describe()

        region_df  = region_df .astype(int)
        st.dataframe(region_df)

        csv = region_df.to_csv(index=True, sep=',')

        st.download_button(label="Download data as CSV",data=csv,file_name='Weekday Performance statistics.csv',mime='text/csv', )


    if st.checkbox('Show Inland Performance Statistics'):


        st.dataframe(df_inland)

        csv = df_inland.to_csv(index=True, sep=',')

        st.download_button(label="Download data as CSV",data=csv,file_name='Inland Performance statistics.csv',mime='text/csv', )


    if st.checkbox('Show Coastal Performance Statistics'):



        st.dataframe(df_coastal)

        csv = df_coastal.to_csv(index=True, sep=',')
        st.download_button(label="Download data as CSV",data=csv,file_name='Coastal Performance statistics.csv',mime='text/csv', )