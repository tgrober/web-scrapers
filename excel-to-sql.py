import pandas as pd
import sqlite3
import sqlalchemy
import pymysql

df = pd.read_excel('xlwt-example.xls',sheet_name='Visa Bulletin For August 2020')
df.replace(r'\s', '', regex = True, inplace = True)

#print(df[['YYY','CHN','IND','MEX','PHL']].dropna())
f1 = df.iloc[0,:].dropna()
#f1 = f1.replace(r'\\n',' ', regex=True)
f2a = df.iloc[1,:].dropna()
f2b = df.iloc[2,:].dropna()
f3 = df.iloc[3,:].dropna()
f4 = df.iloc[4,:].dropna()
#f1_top_row = format.head()
#print(f1_top_row)
print(f1)
print(f1.iloc[0,:])
#print(f2a)
#print(f2b)
#print(f3)
#print(f4)
first_chart = f1 + ' ' + f2a + ' ' + f2b + ' '+ f3 + ' '+ f4 + ' '
#print(first_chart)
chart_id = [2,3,4,5]
pref = ["f1","f2a","f2b","f3"]
cntry = ["YYY","CHN","IND","MEX"]
priority = ["10-12-2006","01-12-2009","12-12-2020","06-12-2004"]
priortiy_sts = ["C","U","C","C"]
# format: mysql://user:pass@host/db
#engine = create_engine('mysql://root:ryan@localhost/visa_bulletin')
#df.to_sql('august_2020', con=engine)

engine = sqlalchemy.create_engine('mysql+pymysql://root:root@localhost/visa_bulletin')
df = pd.read_sql_table('august_2020', engine)
#print(df.head())

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='visa_bulletin')

query_1 = "INSERT INTO `august_2020`(`visa_blltn_chart_id`, `prfrnc_catg`, `cntry_cd`, `prrty_dt`, `prrty_dt_stus`)VALUES(%s, %s, %s, %s, %s)"
#cursor = connection.cursor()
#for i in range(0,3):
#    cursor.execute(query_1,(chart_id[i],pref[i],cntry[i],priority[i],priortiy_sts[i]))

#connection.commit()
