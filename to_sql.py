from sqlalchemy import create_engine
import pandas as pd
from GS.GS import GS_to_DF

creds='GS/test_sheets_client_secret.json'
url='https://docs.google.com/spreadsheets/d/........./edit?pli=1#gid=0

df1=GS_to_DF(url=url,sheet=sheet1,credenciales=creds)
df2=GS_to_DF(url=url,sheet=sheet2,credenciales=creds)


#SUBIR A MYSQL
#creo la conexion a mysql y le digo la tabla sobre la que voy a trabajar
engine = create_engine('mysql+pymysql://dbiadmin:myaccount@mysql.site.com:3306/user?charset=utf8mb4&binary_prefix=true', echo=False)
conn = engine.connect()
trans = conn.begin()
table1 = 'table1name'
table2 = 'table2name'
#creo una tabla temporal en donde voy a poner los días que quiero borrar de la tabla original
df1.to_sql(name= table1, con=engine, if_exists = 'replace', index=False)
df2.to_sql(name= table2, con=engine, if_exists = 'replace', index=False)

#borro la info vieja que tengo que reemplazar usando la tablita de temp que cree antes tomando la fecha referencia
#engine.execute("delete from "+tabla_DCM+" where Date in (select Date from temp)")
#engine.execute("insert into "+tabla_DCM+" (select * from temp)")
#engine.execute("drop table if exists temp")
#trans.commit()
