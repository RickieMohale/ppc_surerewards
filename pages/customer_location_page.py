



#select latitude,longitude from userlocations
df = pd.DataFrame(np.random.randn(1000, 2) / [1, 1] + [-25.99, 28.13],
columns=['lat','lon'])
#[-25.993138, 28.128150]
position = pd.read_sql_query("select latitude as lat,longitude as lon from userlocations",conn)



st.map(position )
