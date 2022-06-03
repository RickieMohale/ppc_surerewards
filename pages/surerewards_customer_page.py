




st.markdown("<h1 style='text-align: center; color: red;'>Surerewards Customers Insights Page</h1>", unsafe_allow_html=True)










col1, col2 = st.columns((1,1))

with col1:

    st.info("The following visuals are based on real time data from the surerewards platform (They change with time)")
    
with col2:
    ## Show the latest Update Time
    from datetime import datetime
    SA_time = pytz.timezone('Africa/Johannesburg') 
    datetime_SA = datetime.now(SA_time)
    metric("Latest Time Update", datetime_SA.strftime('%Y-%m-%d %H:%M %p'))







# Loaading Datasets
num_bags =pd.read_sql_query("select cast(r.updatedAt as date) as date,sum(ppc_surebuild + ppc_surecast + ppc_surecem + ppc_suretech + ppc_surewall) as number_of_bags from receipts as r inner join receiptdata as rdata on r.id =rdata.receipt_id where r.status in ('approved','Limit reached.') and cast(r.updatedAt as date)  >= '2022-02-15'  group by date" ,conn)


######################################  Registration ################################
num_reg =pd.read_sql_query(" Select count(*) as number_of_registration,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15' group by date ",conn)
num_reg_promo =pd.read_sql_query(" Select count(*) as number_of_registration,cast(createdAt as date) as date  from users where code != 'PPC130' and  cast(createdAt as date) >= '2022-02-15' group by date ",conn)



#### adding zeros to days where customers did not apply the promo 
for i in list(num_reg['date']):
    if i not in list(num_reg_promo['date']):
        num_reg_promo.loc[len(num_reg_promo.index)]= [0,i]

num_reg_promo = num_reg_promo.sort_values(by="date")


########### describing registration and PPC130 
num_reg['description'] = 'No of Registration'
num_reg_promo['description'] = 'PPC130 Opt-in'




###########################################################################################

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


sms_numbers=pd.read_sql_query("select count(*) as Number_Of_SMS_Sent ,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date)>='2022-02-15' group by date order by date",conn)

sms_numbers_on_date=pd.read_sql_query("select type,body,cast(createdAt as date) as date from sms where body !='' and cast(createdAt as date)>='2022-02-15'",conn)


    
## Number of registration Visual


## Number of registration receipts upload







	








#chart = alt.Chart(chart_data).mark_area(line={'color':'darkgreen'},color=alt.Gradient(gradient='linear',stops=[alt.GradientStop(color='white', offset=0),alt.GradientStop(color='darkgreen', offset=1)],x1=1,x2=1,y1=1,y2=0)).encode(x = 'date',y = 'num_of_reg')












st.markdown("<h3 style='text-align: center; color: red;'>Number of  Customers</h3>", unsafe_allow_html=True)






########################## description ##########################3
container = st.container()
col1, col2= st.columns(2)

with container:
    with col1:
        st.info( "Existing customers is customers who registered before 15-Feb-2-2022 ")	

    with col2:
        st.info( "PPC130 customers is customers who registered from 15-Feb-2-2022")
########################################################################3





num_receipts_bar=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where code !='PPC130' and status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','Approved','Limit reached.') and cast(receipts.updatedAt as date) >='2022-02-15'  ",conn)
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










total_ex_active = pd.read_sql_query("SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where status  in ('Duplicate receipts','outdated Receipt','Receipt cut off.','Receipt not relevant', 'Receipt not visible','approved','Limit Reached.') and cast(receipts.updatedAt as date) >='2022-02-15' and cast(users.createdAt as date ) <= '2022-02-15'",conn)

prev_month_ex_active =pd.read_sql_query("SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(receipts.updatedAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' ) and cast(users.createdAt as date ) <= '2022-02-15' ",conn)

yesterday_ex_active =pd.read_sql_query( "SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date)= DATE_SUB(CURDATE(), INTERVAL 1 DAY) and cast(users.createdAt as date ) <= '2022-02-15'",conn)

week_ex_active = pd.read_sql_query( "SELECT count(distinct(users.id)) as count from users inner join receipts on users.id=receipts.user_id where week(receipts.updatedAt) = week(DATE_SUB(CURDATE(), INTERVAL 0 DAY))-1 and cast(users.createdAt as date ) <= '2022-02-15'",conn)


## Ensuring that daily conversion takes in zero ########
list_ =list(yesterday_ex_active.columns)


### Get todays date  ##########
from datetime import datetime, timedelta
yest_date= datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

################################










total_reg_prev_month = pd.read_sql_query("SELECT count(*) as count from users where cast(createdAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(createdAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' )",conn)

prev_day_reg =pd.read_sql_query("SELECT count(*) as count from users where cast(createdAt as date)=DATE_SUB(CURDATE(), INTERVAL 1 DAY)",conn)
prev_week_reg= pd.read_sql_query("SELECT count(*) as count from users where week(createdAt) = week(DATE_SUB(CURDATE(), INTERVAL 0 DAY))-1",conn)




prev_month_recpt =pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload  from users inner join receipts on users.id=receipts.user_id where cast(users.createdAt as date)>= DATE_FORMAT( CURRENT_DATE - INTERVAL 1 MONTH, '%Y/%m/01' ) and cast(users.createdAt as date)< DATE_FORMAT( CURRENT_DATE, '%Y/%m/01' )",conn)

prev_week_recpt =pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload from users inner join receipts on users.id=receipts.user_id where  week(users.createdAt) = week(DATE_SUB(CURDATE(), INTERVAL 0 DAY))-1",conn)

prev_day_rcpt=pd.read_sql_query("SELECT count(distinct(users.id)) as no_of_receipts_upload from users inner join receipts on users.id=receipts.user_id where  cast(users.createdAt as date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)",conn)









total_sms_date =len(list(sms_numbers_on_date['body']))
withdrawm_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('withdraw')]['body'].count()
succes_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('successfully captured')]['body'].count()
less_bag_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('Miss Out')]['body'].count()



st.info ('A total  of '+ str( sms_numbers['Number_Of_SMS_Sent'].sum() )+' SMSes have been sent during the PPC130 campaign.From the SMSes sent ,'+str(withdrawm_no)+' was about withdrawal request,which is '+str(round((withdrawm_no/total_sms_date)*100))+'% of the total SMS sent.'+str(succes_no )+' was about successfully captured receipts, which is '+str(round((succes_no/total_sms_date)*100))+'%  of the total SMS sent.'+str(less_bag_no)+' was SMS sent to customers who bought less than 10 bags, which is '+str(round((less_bag_no/total_sms_date)*100))+'%  of the total SMS sent.')




#options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Pressure","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10,},},"progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value": 50, "name": "Score"}],}],}


#options = {"tooltip" : {"formatter": "{a} <br/>{b} : {c}%"},"toolbox": {"show": "true","feature" : {"mark" : {"show": "true"},"restore" : {"show":"true"},"saveAsImage" : {"show": "true"}}},"series" : [{"name":'Conversion rate',"type":'gauge',"splitNumber": 10, "axisLine": { "lineStyle": { "color": [[0.2, '#228b22'],[0.8, '#48b'],[1, '#ff4500']],"width": 8}},"axisTick": {"splitNumber": 10,"length" :12, "lineStyle": {"color": 'auto'}},"axisLabel": {"textStyle": {"color": 'auto'}},"splitLine": {"show": "true","length" :30,"lineStyle": { "color": 'auto'}},"pointer" : {"width" : 5},"title" : {"show" :"true","offsetCenter": [0, '-40%'],"textStyle": {"fontWeight": 'bolder'}},"detail" : {"formatter":'{value}%',"textStyle": {"color": 'auto',"fontWeight": 'bolder'}},"data":[{"value": 50, "name": 'eteva '}]}]}

#options = {"tooltip" : {"formatter": "{a} <br/>{b} : {c}%" },"toolbox": {"show" : "true","feature" : {"mark" : {"show": "true"},"restore" : {"show": "true"},"saveAsImage" : {"show": "true"}}},"series" : [{"name":'Conversion rate',"type":'gauge',"splitNumber": 10,"axisLine": {"lineStyle": {"color": [[0.2, '#228b22'],[0.8, '#48b'],[1, '#ff4500']],"width": 8}},"axisTick": {"splitNumber": 10,"length":12,"lineStyle": {"color": 'auto'}},"axisLabel": {"textStyle": {"color": 'auto'}},"splitLine": { "show": "true","length" :30,"lineStyle": {"color": 'auto'}},"pointer" : {"width" : 5},"title" : {"show" : "true","offsetCenter": [0, '-40%'],"textStyle": {"fontWeight": 'bolder'}},"detail" : {"formatter":'{value}%',"textStyle": {"color": 'auto',"fontWeight": 'bolder'}},"data":[{"value": 50, "name": 'eteva '}]}]}

#st_echarts(options=options, width="100%", key=10)  
            


############################# New Charts #####################################################


num_reg_ =pd.read_sql_query(" Select count(*) as num_of_reg,cast(createdAt as date) as date  from users where cast(createdAt as date) >= '2022-02-15'  ",conn)
num_receipts=pd.read_sql_query("SELECT count(*) as no_of_receipts_upload ,cast(receipts.updatedAt as date) as date from users inner join receipts on users.id=receipts.user_id where cast(receipts.updatedAt as date) >='2022-02-15' group by date ",conn)



######################################## Registration Chart ######################

dates =[str(x) for x in num_reg['date'].tolist()]

reg_chart = {"title": {"text": 'Customer Registration',"left": 'center'},"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' }}},
"tooltip": {"trigger": 'axis',"axisPointer": {"type": 'cross',"label": {"backgroundColor": '#6a7985'}}},
"legend": {"data": ['PPC130 Opt-In','Number Of Registration'],"left":40,"top":20},"grid": {"left": '3%',"right": '4%',"bottom":"15%","containLabel":"true" },"dataZoom": [{"show": "true","realtime": "true",
"start": 65,"end": 85},{"type": 'inside',"realtime": "true","start": 65,"end": 85}],"xAxis": [{"type": 'category',"boundaryGap": "false","data": dates}],"yAxis": [{"type": 'value'}],
"series": [{"name":'PPC130 Opt-In',"type": 'line',"stack": 'Total',"areaStyle": {},"emphasis": {"focus": 'series'},
"data": num_reg_promo['number_of_registration'].tolist()},{"name": 'Number Of Registration',"type": 'line',"stack": 'Total',"areaStyle": {},
"emphasis": {"focus": 'series'},"data": num_reg['number_of_registration'].tolist()}]}
#####################################################################################################


########################## Reciepts Upload ########################################

dates =[str(x) for x in num_receipts['date'].tolist()]

recpt_up_chart = {"title": {"text": 'Receipt Upload',"left": 'center'},"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' }}},
"tooltip": {"trigger": 'axis',"axisPointer": {"type": 'cross',"label": {"backgroundColor": '#6a7985'}}},
"grid": {"left": '3%',"right": '4%',"bottom": '20%',"containLabel":"true" },"dataZoom": [{"show": "true","realtime": "true",
"start": 65,"end": 85},{"type": 'inside',"realtime": "true","start": 65,"end": 85}],"xAxis": [{"type": 'category',"boundaryGap": "false","data": dates}],"yAxis": [{"type": 'value'}],
"series": [{"name":'No Of Receipts',"type": 'line',"stack": 'Total',"areaStyle": {},"emphasis": {"focus": 'series'},
"data": num_receipts["no_of_receipts_upload"].tolist()}]}



#  "title": {"text": 'Stacked Area Chart'},  

#"grid": {"bottom": 100},


#"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' },"restore": {},"saveAsImage": {}}}

#: [{"type": 'time', "axisLabel": {formatter: function (num_reg['date'].tolist()) {return echarts.format.formatTime('yyyy-MM-dd', value)}

col1, col2 = st.columns((1,1))
with col1:

    st_echarts(options=reg_chart, width="100%", key=0)  
with col2:
    st_echarts(recpt_up_chart , width="100%", key=1)  




##################### Second Charts   ################################

#st.dataframe(num_reg_total['num_of_reg'].sum())
#st.write('The current number is ',int(num_reg_total['num_of_reg'].sum()))

########################################  Number Of Customers ###############
no_customers_chart = {"title": {"text": 'Number Of  Customers',"left": 'center'},'tooltip': {'trigger': 'axis','axisPointer': {'type': 'shadow'}},'grid': {'left': '3%','right': '4%','bottom': '3%','containLabel': 'true'},
'xAxis': [{'type': 'category','data': ["Surerewards Customers", "Existing Customers","PPC130 Campaign Customers", "Customers With PPC130 Code"],'axisTick': {'alignWithLabel': 'true'},"axisLabel": {"width": 100,"overflow": "truncate","interval": 0,"rotate": 30 }}],'yAxis': [{'type': 'value' }],
'series': [{'name': 'Direct','type': 'bar','barWidth': '60%','data':[int(num_reg_total['num_of_reg'].sum()),int(existing_reg['num_of_reg'].sum()),int(num_reg_['num_of_reg'].sum()),int(num_promo_reg['No_Promocode'].sum())]}],"label": {"show": "true","position": 'top',"valueAnimation": "true"}}


###################################################################




###################################### Number Of  Receipts ###############################

no_recpt_chart = {"title": {"text": 'Customer Engagement',"left": 'center'},'tooltip': {'trigger': 'axis','axisPointer': {'type': 'shadow'}},'grid': {'left': '3%','right': '4%','bottom': '3%','containLabel': 'true'},
'xAxis': [{'type': 'category','data': ["Surerewards Customers With Recipets Upload", "PPC130 Customers With Recipets Upload" , "Surerewards Customers With Valid Recipets", "PPC130 Customers With Valid Recipets "],'axisTick': {'alignWithLabel': 'true'},"axisLabel": {"width": 100,"overflow": "truncate","interval": 0,"rotate": 30 }}],'yAxis': [{'type': 'value' }],
'series': [{'name': 'Direct','type': 'bar','barWidth': '60%','data': [ int(num_user_r_upload_total['no_of_receipts_upload'].sum()),int(num_user_r_upload['no_of_receipts_upload'].sum()),int(num_user_valid_receipts_total["no_of_users_valid_receipts"].sum()), int(num_user_valid_receipts["no_of_users_valid_receipts"].sum())]}],"label": {"show": "true","position": 'top',"valueAnimation": "true"}}



col1, col2 = st.columns((1,1))
with col1:

    st_echarts(options=no_customers_chart, width="100%", key=3)      
    
with col2:
    st_echarts(options=no_recpt_chart , width="100%", key=4) 




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


container = st.container()
col1, col2= st.columns(2)

with container:
    
    with col1:
        
        options = { "tooltip": {"trigger": 'axis', "axisPointer": {"type": 'shadow'  }},"legend": {},
        "grid": {"left": '3%', "right": '4%',"bottom": '3%',"containLabel": "true" },"yAxis": {"type": 'value'},"xAxis": {"type": 'category',"data": ['Total', 'Valid', 'Invalid']},
        "series": [{"name": 'With PPC130', "type": 'bar',"stack": 'total', "label": {"show": "true"},"emphasis": {"focus": 'series' },"data":[int(num_promo_receipts['no_of_receipts_upload'].sum()),int(num_valid_promo_receipts["no_of_valid_receipts"].sum()),int(num_invalid_promo_receipts["no_of_invalid_receipts"].sum())] },
        {"name": 'Without PPC130 ',"type": 'bar',"stack": 'total', "label": {"show": "true"},"emphasis": {"focus": 'series'},"data":[int(num_receipts_bar['no_of_receipts_upload'].sum()), int(num_valid_receipts["no_of_valid_receipts"].sum()), int(num_invalid_receipts["no_of_invalid_receipts"].sum()) ]}]}

        st_echarts(options=options, width="100%", key=20) 

    with col2:

        optin = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
        "restore": { "show": "true" }}}, "series": [ { "name": 'Receipt Validation', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
        "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value": int(status['count'][0]), "name": status['status'][0] },{ "value":int(status['count'][1]), "name": status['status'][1]},{ "value":int(status['count'][2]), "name": status['status'][2]},{ "value":int(status['count'][3]), "name": status['status'][3]},{ "value":int(status['count'][4]), "name": status['status'][4]},{ "value":int(status['count'][5]), "name": status['status'][5]},{ "value":int(status['count'][6]), "name": status['status'][6]}]}]}
        st_echarts(options=optin, width="100%", key=19) 





st.markdown("<h3 style='text-align: center; color: red;'>PPC130 Customer Conversion</h3>", unsafe_allow_html=True)









ovr_con_rate = round(float(num_user_r_upload['no_of_receipts_upload'].sum() /num_reg_['num_of_reg'].sum())*100,2)
last_mon_rate = round(float(prev_month_recpt["no_of_receipts_upload"].sum()/total_reg_prev_month["count"].sum())*100,2)
weekly_con_rate = round(float(prev_week_recpt["no_of_receipts_upload"].sum()/prev_week_reg['count'].sum())*100,2)
yest_con_rate = round(float(prev_day_rcpt["no_of_receipts_upload"].sum()/ prev_day_reg["count"].sum())*100,2)








container = st.container()
col1, col2= st.columns(2)

with container:
    
    with col1:
        
        option = { "tooltip": { "trigger": 'axis', "axisPointer": { "type": 'shadow'}},"legend": {},"grid": {"left": '3%',"right": '4%',"bottom": '3%',"containLabel": "true"},"xAxis": {"type": 'value',"boundaryGap": [0, 0.01]},
        "yAxis": {"type": 'category',"data": ['Previous Month', 'Previous week', 'Previous Day', ]},
        "series": [{"name": 'Customer Registration',"type": 'bar',"data": [ int(total_reg_prev_month["count"].sum()), int(prev_week_reg['count'].sum()), int(prev_day_reg["count"].sum())]},{"name": 'Receipt Upload',"type": 'bar',"data": [int(prev_month_recpt["no_of_receipts_upload"].sum()),int(prev_week_recpt["no_of_receipts_upload"].sum()),int(prev_day_rcpt["no_of_receipts_upload"].sum())]}]}
        st_echarts(options=option, width="100%", key=18) 
                


    with col2:
        
        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":ovr_con_rate, "name": "Score"}],}],}
        st_echarts(options=options, width="100%", key=11),
        st.markdown("<h6 style='text-align: center; color: black;'>Overall Conversion Rate During PPC130 Campaign</h6>", unsafe_allow_html=True)




container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":last_mon_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=111),
        st.markdown("<h6 style='text-align: center; color: black;'>last Month's Conversion Rate</h6>", unsafe_allow_html=True) 

    with col2:

        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":weekly_con_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=12) 
        st.markdown("<h6 style='text-align: center; color: black;'>last Weeks's Conversion Rate</h6>", unsafe_allow_html=True) 
    
    with col3:

        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":yest_con_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=14) 
        st.markdown("<h6 style='text-align: center; color: black;'>yesterday's Conversion Rate</h6>", unsafe_allow_html=True) 





st.info( "PPC130 customer conversion is calcuated by the number of existing users who uploaded a receipts against the total number of registration")


st.markdown("<h3 style='text-align: center; color: red;'>Existing Customer Conversion</h3>", unsafe_allow_html=True)








e_ovr_con_rate = round(float(total_ex_active['count'].sum() /existing_reg['num_of_reg'].sum())*100,3)
e_last_mon_rate = round(float(prev_month_ex_active['count'].sum()/existing_reg['num_of_reg'].sum())*100,3)
e_weekly_con_rate = round(float(week_ex_active['count'].sum()/existing_reg['num_of_reg'].sum())*100,3)
e_yest_con_rate = round(float(yesterday_ex_active['count'].sum()/existing_reg['num_of_reg'].sum())*100,3)




container = st.container()
col1,col2,col3= st.columns((1,1,2))

with container:
    with col1:

        metric("Total Active Existing Users During PPC130 Campaint", total_ex_active['count'].sum())
        metric("Active Existing Users last Week", week_ex_active['count'].sum() )



    with col2:

        metric("Active Existing Users last Month", prev_month_ex_active['count'].sum())
        metric("Active Existing Users yesterday ( "+str(yest_date)+" )" , yesterday_ex_active['count'].sum() )
    
    with col3:

        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":e_ovr_con_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=118),
        st.markdown("<h6 style='text-align: center; color: black;'>Overall Conversion Rate</h6>", unsafe_allow_html=True) 




container = st.container()
col1, col2,col3= st.columns(3)

with container:
    with col1:
        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":e_last_mon_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=15),
        st.markdown("<h6 style='text-align: center; color: black;'>last Month's Conversion Rate</h6>", unsafe_allow_html=True) 

    with col2:

        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":e_weekly_con_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=16) 
        st.markdown("<h6 style='text-align: center; color: black;'>last Weeks's Conversion Rate</h6>", unsafe_allow_html=True) 
    
    with col3:

        options = {"tooltip": {"formatter": "{a} <br/>{b} : {c}%"},"series": [{"name": "Conversion Rate","type": "gauge","axisLine": {"lineStyle": {"color": [[0.2, '#FF0000'],[0.8, '#1e90ff'],[1, '#009900']],"width": 10},},
        "progress": { "width": 10},"detail": {"valueAnimation": "true", "formatter": "{value}"},"data": [{"value":e_yest_con_rate, "name": "Score"}],}],}

        st_echarts(options=options, width="100%", key=17) 
        st.markdown("<h6 style='text-align: center; color: black;'>yesterday's Conversion Rate</h6>", unsafe_allow_html=True) 









####################################### #####################################################################











    ##############  Reciept Upload #############################





#"option = {
#  tooltip: {trigger: 'item'},legend: {top: '5%',left: 'center'},series: [{name: 'Access From',type: 'pie', radius: ['40%', '70%'],
#      avoidLabelOverlap: false,
#      itemStyle: {
#        borderRadius: 10,borderColor: '#fff',borderWidth: 2},label: {show: false,position: 'center'},emphasis: {label: {
 #       show: true,fontSize: '40',fontWeight: 'bold'}},labelLine: {show: false
#      },
#      data: [
 #       { value: 1048, name: 'Search Engine' },
 #       { value: 735, name: 'Direct' },
 #       { value: 580, name: 'Email' },
#        { value: 484, name: 'Union Ads' },
#        { value: 300, name: 'Video Ads' }
#      ]
#    }
#  ]"
#}

#optin = {  "legend": {"top": 'bottom'},"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
#"restore": { "show": "true" },"saveAsImage": { "show": "true" }}}, "series": [ { "name": 'Nightingale Chart', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
#"roseType": 'area',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value": int(10), "name": status['status'][0] },{ "value":int(20), "name": status['status'][1]},{ "value":int(40), "name": status['status'][2]},{ "value":int(70), "name": status['status'][3]},{ "value":int(89), "name": status['status'][4]},{ "value":int(49), "name": status['status'][5]},{ "value":int(20), "name": status['status'][6]}]}]}
#st_echarts(options=optin, width="100%", key=21) 






total_sms_date =len(list(sms_numbers_on_date['body']))
withdrawm_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('withdraw')]['body'].count()
succes_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('successfully captured')]['body'].count()
less_bag_no =sms_numbers_on_date[sms_numbers_on_date['body'].str.contains('Miss Out')]['body'].count()



 
container = st.container()
col1, col2= st.columns(2)

with container:
    with col1:

        dates =[str(x) for x in sms_numbers['date'].tolist()]

        sms_chart = {"title": {"text": 'Customer Communication By SMS',"left": 'center'},"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' }}},
        "tooltip": {"trigger": 'axis',"axisPointer": {"type": 'cross',"label": {"backgroundColor": '#6a7985'}}},
        "grid": {"left": '3%',"right": '4%',"bottom": '20%',"containLabel":"true" },"dataZoom": [{"show": "true","realtime": "true",
        "start": 65,"end": 85},{"type": 'inside',"realtime": "true","start": 65,"end": 85}],"xAxis": [{"type": 'category',"boundaryGap": "false","data": dates}],"yAxis": [{"type": 'value'}],
        "series": [{"name":'No Of SMSes Sent',"type": 'line',"stack": 'Total',"areaStyle": {},"emphasis": {"focus": 'series'},
        "data": sms_numbers['Number_Of_SMS_Sent'] .tolist()}]}
        st_echarts(sms_chart , width="100%", key=23)  
    with col2:
        
        sms_split = {"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
        "restore": { "show": "true" }}}, "series": [ { "name": 'Receipt Validation', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
        "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value": int(withdrawm_no), "name": 'withdrawal SMS' },{ "value":int(succes_no), "name": 'Successfully Captured SMS'},{ "value":int(less_bag_no), "name": 'SMS For Less Than 10 bags'}]}]}
        st_echarts(options=sms_split, width="100%", key=24) 





st.markdown("<h3 style='text-align: center; color: red;'>Customer Money Withdrwals</h3>", unsafe_allow_html=True)


withdraw_by_date =pd.read_sql_query("select sum(amount) as amount, cast(createdAt as date) as date from withdrawals group by date",conn)







wthdrwal_amaount_type = pd.read_sql_query("select type as withdraw_type,sum(amount) as amount from withdrawals group by withdraw_type",conn)

None_amount = wthdrwal_amaount_type[wthdrwal_amaount_type['withdraw_type']=='']['amount'].reset_index()
ewallet_amount = wthdrwal_amaount_type[wthdrwal_amaount_type['withdraw_type']=='e-wallet']['amount'].reset_index()
account_amount = wthdrwal_amaount_type[wthdrwal_amaount_type['withdraw_type']=='account']['amount'].reset_index()




container = st.container()
col1, col2= st.columns((2,1))

with container:
    with col1:
        
        dates =[str(x) for x in withdraw_by_date['date'].tolist()]

        withdraw_chart = {"title": {"text": 'Customer Withdrawal Amount',"left": 'center'},"toolbox": {"feature": {"dataZoom": {"yAxisIndex": 'none' }}},
        "tooltip": {"trigger": 'axis',"axisPointer": {"type": 'cross',"label": {"backgroundColor": '#6a7985'}}},
        "grid": {"left": '3%',"right": '4%',"bottom": '20%',"containLabel":"true" },"dataZoom": [{"show": "true","realtime": "true",
        "start": 65,"end": 85},{"type": 'inside',"realtime": "true","start": 65,"end": 85}],"xAxis": [{"type": 'category',"boundaryGap": "false","data": dates}],"yAxis": [{"type": 'value'}],
        "series": [{"name":'Withdrawal Amount',"type": 'line',"stack": 'Total',"areaStyle": {},"emphasis": {"focus": 'series'},
        "data": withdraw_by_date['amount'] .tolist()}]}
        st_echarts(withdraw_chart , width="100%", key=25)

  
    with col2:


        amaount_type = {"title": {"text": 'Withdrawal Amount Vs Type',"left": 'center'},"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
        "restore": { "show": "true" }}}, "series": [ { "name": 'Withdrawal Amount', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
        "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value":  None_amount['amount'][0], "name": 'No Description' },{ "value": ewallet_amount['amount'][0], "name": 'E-Wallet'},{ "value":account_amount['amount'][0], "name": 'Bank Account'}]}]}
        st_echarts(options=amaount_type, width="100%", key=26) 



wthdrwal_count_type = pd.read_sql_query("select type as withdraw_type, count(*) as count from withdrawals group by withdraw_type",conn)
None_count=  wthdrwal_count_type[ wthdrwal_count_type['withdraw_type']=='']['count'].reset_index()
ewallet_count =  wthdrwal_count_type[wthdrwal_count_type ['withdraw_type']=='e-wallet']['count'].reset_index()
account_count =  wthdrwal_count_type[ wthdrwal_count_type['withdraw_type']=='account']['count'].reset_index()




container = st.container()
col1,col2,col3,col4= st.columns((1,1,1,2))

with container:
    with col1:

        metric("Total Withdrawal Amount",  withdraw_by_date['amount'].sum() )
        metric("Last Month  Withdrawal Amount", 0 )



    with col2:

        metric("Total Number of Withdrawls", int(None_count['count'][0]+ewallet_count['count'][0]+account_count['count'][0]) )
        metric("Last Week Withdrawal Amount" ,  0 )

    with col3:

        metric("Aearage Withdrawl Amount",  round(withdraw_by_date['amount'].mean(),2) )
        metric("Yesterday Withdrawal Amount", 0 )
  
 
    with col4:


        count_type = {"title": {"text": 'Withdrawal Count Vs Type',"left": 'center'},"tooltip": {"trigger": 'item', "formatter": '{a} <br/>{b} : {c} ({d}%)' },"toolbox": {"show": "true","feature": {"mark": { "show": "true" },"dataView": { "show": "true", "readOnly": "false" },
        "restore": { "show": "true" }}}, "series": [ { "name": 'Withdrawal Amount', "type": 'pie', "radius": [50, 100],"center": ['50%', '50%'],
        "roseType": '',"itemStyle": {"borderRadius": 8},"label": {"show": "false"},"emphasis": {"label": {"show": "true"}},"data": [{ "value": int(None_count['count'][0]), "name": 'No Description' },{ "value": int(ewallet_count['count'][0]), "name": 'E-Wallet'},{ "value":int(account_count['count'][0]), "name": 'Bank Account'}]}]}
        st_echarts(options=count_type, width="100%", key=27) 
