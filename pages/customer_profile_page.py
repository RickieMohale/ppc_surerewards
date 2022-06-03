



df_receiptdata= pd.read_sql_query("select mechant,location,profile_user_id as user_id,business_type as occupation,sum(ppc_surebuild) as ppc_surebuild ,sum(ppc_surecem) as ppc_surecem ,sum(ppc_surecast) as ppc_surecast ,sum(ppc_suretech) as ppc_suretech ,sum(ppc_surewall) as ppc_surewall ,sum(ppc_sureroad) as ppc_sureroad ,sum(ppc_plaster) as ppc_plaster,sum(ppc_motor) as ppc_mortar from profiles as p inner join receipts as r on p.profile_user_id=r.user_id inner join receiptdata  as rdata on r.id=rdata.receipt_id where status in ('approved','Limit reached.') and business_type!='' group by profile_user_id order by ppc_surebuild ",conn)

### split data into city and province
df_receiptdata[['city','province','mixed_location']] = df_receiptdata['location'].str.split(',', expand=True)
df_receiptdata.drop('location', axis=1, inplace=True)


#Removing white spaces
df_receiptdata['city'] = df_receiptdata['city'].str.strip() 
df_receiptdata['province'] = df_receiptdata['province'].str.strip()
df_receiptdata['mechant'] = df_receiptdata['mechant'].str.strip()
df_receiptdata['occupation'] = df_receiptdata['occupation'].str.strip() 
#lowering all letters
df_receiptdata['city'] =df_receiptdata['city'].str.lower()
df_receiptdata['province'] = df_receiptdata['province'].str.lower()
df_receiptdata['mechant'] = df_receiptdata['mechant'].str.lower()

df_receiptdata['occupation'] =df_receiptdata['occupation'].str.lower()
#Removing all punctuations

df_receiptdata['city'] =df_receiptdata['city'].str.replace(r'[^\w\s]+', '', regex=True)
df_receiptdata['province'] = df_receiptdata['province'].str.replace(r'[^\w\s]+', '', regex=True)
df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace(r'[^\w\s]+', '', regex=True)
df_receiptdata['occupation'] =df_receiptdata['occupation'].str.replace(r'[^\w\s]+', '', regex=True)

#Removing all numbers from strings

df_receiptdata['city'] =df_receiptdata['city'].str.replace('\d+', '', regex=True)
df_receiptdata['province'] = df_receiptdata['province'].str.replace('\d+', '', regex=True)
df_receiptdata['mechant'] = df_receiptdata['mechant'].str.replace('\d+', '', regex=True)
df_receiptdata['occupation'] =df_receiptdata['occupation'].str.replace('\d+', '', regex=True)


df_receiptdata['Total number of bags'] =df_receiptdata['ppc_surebuild']+df_receiptdata['ppc_surecem'] +df_receiptdata['ppc_surecast']+df_receiptdata['ppc_suretech']+df_receiptdata['ppc_surewall']+df_receiptdata['ppc_sureroad']+df_receiptdata['ppc_plaster']+df_receiptdata['ppc_mortar']
df_receiptdata = df_receiptdata[df_receiptdata['Total number of bags']>0]
##########Cleaning #################################\

province_name =['limpopo','gauteng','mpumalanga','north west','free state','western cape','eastern cape','kwazulu natal','northern cape']


##### Replacing province name with true province name ################3

df_receiptdata=replace_similar_words(df_receiptdata,'province',province_name,80)


##### Replacing incorrect province with mode


prov_mode =df_receiptdata['province'].mode()[0]

for i,row in df_receiptdata.iterrows():
    if df_receiptdata.at[i,'province'] not in province_name :
        df_receiptdata.at[i,'province'] =prov_mode



##################################################



tpyes_occp_df = pd.read_sql_query("select distinct(profile_user_id) as user_id,business_type as occupation  from profiles where business_type!=''",conn)


occup_recpt_df= pd.read_sql_query("select count(distinct(profile_user_id)) as count from profiles as p inner join receipts as r on p.profile_user_id=r.user_id inner join receiptdata  as rdata on r.id=rdata.receipt_id where  business_type!='' ",conn)



########################### Customers With Occupation ##########################


container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        metric("Customers with occupation entries",  tpyes_occp_df['user_id'].count())

    with col2:
        metric(" Customers with occupation entries and receipts Upload" ,occup_recpt_df['count'].sum())

    with col3:
        metric("Customers with occupation entries and valid receipts Upload" ,len(df_receiptdata['user_id'] ) )






#########################################################3



st.markdown("<h3 style='text-align: center; color: red;'>Customer Profiling By Occupatipon</h3>", unsafe_allow_html=True)





product_name = ['ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_mortar']

options = st.multiselect('Select Product', product_name,['ppc_surebuild'])



        
occ_freq_dict = unique_names(df_receiptdata['occupation'])
data = {'Occupation': occ_freq_dict.keys(), 'Occupation Frequency': occ_freq_dict.values()}
occ_freq_dict  = pd.DataFrame.from_dict(data)


plot_df_occ =occ_freq_dict.head(20)
plot_df_occ=plot_df_occ.sort_values('Occupation Frequency', ascending=True)



st.info(" The visual below allows you to select a product and find out which type of customer allows  buys that product")

container = st.container()
col1, col2= st.columns((1, 1))

with container:
    with col1:

        name_ = ['Total number of bags','ppc_surebuild','ppc_surecem','ppc_surecast','ppc_suretech','ppc_surewall','ppc_sureroad','ppc_plaster','ppc_mortar']

        df =df_receiptdata.groupby(['occupation'])[options+['Total number of bags']].apply(lambda x : x.astype(int).sum())

        
        df['occupation'] = df.index

        df= df[df['occupation']!='na']
        df= df[df['occupation']!='none']
        
        

        

       


        df=df.sort_values('Total number of bags', ascending=False)
        df=df.head(20)

        df = df.sort_values('Total number of bags', ascending=True)
        df= df.drop(['Total number of bags'], axis = 1)



        ax = df.plot.barh(stacked=True,figsize=(10,5))
        # add labels
        ax.legend(loc='lower right')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_ylabel("Occupation")
        ax.set_xlabel("Number Of Bags")
        st.pyplot(plt.show())

        



    with col2:
        fig, ax = plt.subplots()
        plt.tight_layout()


        ax.barh(list(plot_df_occ['Occupation']) ,list(plot_df_occ['Occupation Frequency']))

        ax.legend(loc='lower right')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        plt.ylabel('Occupation')
        plt.xlabel('Occupation Frequency')
        st.pyplot(fig)






st.markdown("<h3 style='text-align: center; color: red;'>Customer Location</h3>", unsafe_allow_html=True)


position = pd.read_sql_query("select latitude as lat,longitude as lon from userlocations",conn)



st.map(position )

