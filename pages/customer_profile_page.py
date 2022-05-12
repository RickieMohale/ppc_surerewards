



occupation_df= pd.read_sql_query("select profile_user_id as user_id,business_type as occupation,sum(ppc_surebuild) as ppc_surebuild ,sum(ppc_surecem) as ppc_surecem ,sum(ppc_surecast) as ppc_surecast ,sum(ppc_suretech) as ppc_suretech ,sum(ppc_surewall) as ppc_surewall ,sum(ppc_sureroad) as ppc_sureroad ,sum(ppc_plaster) as ppc_plaster,sum(ppc_motor) as ppc_mortar from profiles as p inner join receipts as r on p.profile_user_id=r.user_id inner join receiptdata  as rdata on r.id=rdata.receipt_id where status in ('approved','Limit reached.') and business_type!='' group by profile_user_id order by ppc_surebuild ",conn)



#Removing white spaces
occupation_df['occupation'] = occupation_df['occupation'].str.strip() 
#lowering all letters
occupation_df['occupation'] =occupation_df['occupation'].str.lower()
#Removing all punctuations
occupation_df['occupation'] =occupation_df['occupation'].str.replace(r'[^\w\s]+', '', regex=True)
#Removing all numbers from strings
occupation_df['occupation'] =occupation_df['occupation'].str.replace('\d+', '', regex=True)



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
        metric("Customers with occupation entries and valid receipts Upload" ,len(occupation_df['user_id'] ) )






#########################################################3



st.markdown("<h3 style='text-align: center; color: red;'>Customer Profiling by Occupatipon</h3>", unsafe_allow_html=True)




#options = st.multiselect("Select Product ",  ['a','b','c'], ['a'])
options = st.multiselect(  'What are your favorite colors', ['Green', 'Yellow', 'Red', 'Blue'],['Yellow', 'Red'])



        
occ_freq_dict = unique_names(occupation_df['occupation'])
data = {'Occupation': occ_freq_dict.keys(), 'Occupation Frequency': occ_freq_dict.values()}
occ_freq_dict  = pd.DataFrame.from_dict(data)


plot_df =occ_freq_dict.head(20)
plot_df=plot_df.sort_values('Occupation Frequency', ascending=True)


fig, ax = plt.subplots()
plt.tight_layout()


ax.barh(list(plot_df['Occupation']) ,list(plot_df['Occupation Frequency']))

ax.legend(loc='lower right')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.ylabel('Occupation')
plt.xlabel('Occupation Frequency')
st.pyplot(fig)