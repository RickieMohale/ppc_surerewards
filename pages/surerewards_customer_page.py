




st.markdown("<h1 style='text-align: center; color: red;'>PPC130 Surerewards Insights</h1>", unsafe_allow_html=True)


# Loaading Datasets
num_bags =pd.read_sql_query("select cast(r.updatedAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  >= '2022-02-15'  group by date" ,conn)

num_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15' group by date ",conn)

existing_reg =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) < '2022-02-15' group by date ",conn)

num_reg_ =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15'  ",conn)
num_reg_total =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users ",conn)

num_promo_reg = pd.read_sql_query("Select cast(createdAt as date) as date,count(*) as No_Promocode from users where code = 'PPC130'   ",conn)

num_receipts_total=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id    ",conn)
num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date) >='2022-02-15' group by date ",conn)

num_valid_receipts_total =pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status in ('Approved','Limit reached.')  ",conn)
num_valid_receipts=pd.read_sql_query("SELECT count(*) as no_of_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status in ('Approved','Limit reached.')  and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)

#num_invalid_receipts=pd.read_sql_query("SELECT count(*) as no_of_invalid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible') and cast(receipts.updatedAt as date) >= '2022-02-15'  group by date",conn)

num_user_r_upload_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id  ",conn)
num_user_r_upload=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where  cast(receipts.updatedAt as date) >= '2022-02-15' ",conn)

num_user_valid_receipts_total=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Approved','Limit reached.')  ",conn)
num_user_valid_receipts=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_users_valid_receipts ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where status  in ('Approved','Limit reached.')  and cast(receipts.updatedAt as date) >= '2022-02-15'  ",conn)



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
col1, col2,col3,col4= st.columns(4)

with container:
    with col1:
        metric(" Total No Of Surerewards Customers ", num_reg_total['num_of_reg'].sum())	

    with col2:
        metric(" No Of Existing Customers",existing_reg['num_of_reg'].sum())
    with col3:
        metric(" No Of Customers from PPC130 Campaign ",num_reg_['num_of_reg'].sum())
    with col4:
        metric("Customers With PPC130 Promo Code",num_promo_reg['No_Promocode'].sum())




########################## description ##########################3
container = st.container()
col1, col2= st.columns(2)

with container:
    with col1:
        st.info( "Existing customers is customers who registered before 15-Feb-2-2022 ")	

    with col2:
        st.info( "PPC130 customers is customers who registered from 15-Feb-2-2022")
########################################################################3



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




st.markdown("<h3 style='text-align: center; color: red;'>Existing Customers Conversion </h3>", unsafe_allow_html=True)

total_ex_active = pd.read_sql_query("SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) >='2022-02-15' and cast(users.createdAt as date ) <= '2022-02-15'",conn)

prev_month_ex_active =pd.read_sql_query("SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(receipts.updatedAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' ) and cast(users.createdAt as date ) <= '2022-02-15' ",conn)

yesterday_ex_active =pd.read_sql_query( "SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date)= current_date()-1 and cast(users.createdAt as date ) <= '2022-02-15'",conn)

week_ex_active = pd.read_sql_query( "SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where week(receipts.updatedAt) = week(current_date())-1 and cast(users.createdAt as date ) <= '2022-02-15'",conn)


## Ensuring that daily conversion takes in zero ########
list_ =list(yesterday_ex_active.columns)


### Get todays date  ##########
from datetime import datetime, timedelta
yest_date= datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

################################



container = st.container()
col1, col2,col3,col4= st.columns(4)

with container:
    with col1:
        metric("Total Active Existing Users During PPC130 Campaing",  total_ex_active['count'].sum() )

    with col2:
        metric("Active Existing Users last Month" ,prev_month_ex_active['count'].sum())
    
    with col3:
        metric("Active Existing Users last Week" ,week_ex_active['count'].sum() )
    
    with col4:
        metric("Active Existing Users yesterday ( "+str(yest_date)+" )" ,yesterday_ex_active['count'].sum())




container = st.container()
col1, col2,col3,col4= st.columns(4)

with container:
    with col1:
         metric("Overall Conversion Rate During PPC130 Campaign",   "{0:.02%}".format(total_ex_active['count'].sum() /existing_reg['num_of_reg'].sum())) 

    with col2:
        metric(" last Month's Conversion Rate" , "{0:.02%}".format(prev_month_ex_active['count'].sum()/existing_reg['num_of_reg'].sum()))
    
    with col3:
        metric("last Week's Conversion Rate" , "{0:.02%}".format(week_ex_active['count'].sum()/existing_reg['num_of_reg'].sum()))
    
    with col4:
        metric(" yesterday's ( "+str(yest_date)+" )  Conversion rate" , "{0:.02%}".format(yesterday_ex_active['count'].sum()/existing_reg['num_of_reg'].sum()))




st.info( "Existing user's conversion rate is calcuated by the number of existing users who uploaded a receipts  during a specific time interval  against the total number of existing users")





st.markdown("<h3 style='text-align: center; color: red;'>PPC130 Customers Conversion </h3>", unsafe_allow_html=True)


total_reg_prev_month = pd.read_sql_query("SELECT count(*) as count from users where cast(createdAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(createdAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' )",conn)

prev_day_reg =pd.read_sql_query("SELECT count(*) as count from users where cast(createdAt as date)=current_date()-1",conn)
prev_week_reg= pd.read_sql_query("SELECT count(*) as count from users where week(createdAt) = week(current_date())-1",conn)




prev_month_recpt =pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload  from users inner join receipts on users.id=receipts.user_id where cast(users.createdAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(users.createdAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' )",conn)

prev_week_recpt =pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload from users inner join receipts on users.id=receipts.user_id where  week(users.createdAt) = week(current_date())-1",conn)

prev_day_rcpt=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload from users inner join receipts on users.id=receipts.user_id where  cast(users.createdAt as date) = current_date()-1",conn)



container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        metric("No of customer registrationin in the previous Month",  total_reg_prev_month["count"].sum() )

    with col2:
        metric("No of Customer registration in the previous week " , prev_week_reg['count'].sum())
    
    with col3:
        metric("No of Customer registration in the previous Day" , prev_day_reg["count"].sum())


container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        metric("No of new customer with receipt uploads - previous Month",  prev_month_recpt["no_of_receipts_upload"].sum())

    with col2:
        metric("No of new customer with receipt uploads - previous week " , prev_week_recpt["no_of_receipts_upload"].sum())
    
    with col3:
        metric("No of new customer with receipt uploads - previous Day" , prev_day_rcpt["no_of_receipts_upload"].sum())



container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        metric("Previous Month Conversion rate",   "{0:.0%}".format(prev_month_recpt["no_of_receipts_upload"].sum()/total_reg_prev_month["count"].sum()) )

    with col2:
        metric("previous Week Conversion rate" , "{0:.0%}".format(prev_week_recpt["no_of_receipts_upload"].sum()/prev_week_reg['count'].sum()))
    
    with col3:
        metric("Previos day Conversion rate" , "{0:.0%}".format(prev_day_rcpt["no_of_receipts_upload"].sum()/ prev_day_reg["count"].sum()))

st.info( "PPC130 customer conversion is calcuated by the number of existing users who uploaded a receipts against the total number of registration")





#chart = alt.Chart(status).mark_arc(innerRadius=50).encode(theta=alt.Theta(field="count", type="quantitative"), color=alt.Color(field="status", type="nominal"),)
#st.altair_chart(chart, use_container_width=True)

# Setting size in Chart based on
# given values

st.markdown("<h3 style='text-align: center; color: red;'>PPC130 Receipt Validation</h3>", unsafe_allow_html=True)



container = st.container()
col1, col2= st.columns(2)

with container:
    with col1:
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

    with col2:
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

