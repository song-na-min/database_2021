# -*- coding: utf-8 -*- 
import pymysql
import csv

conn = pymysql.connect(host='localhost',
                        port = 3306,
                        user='root',
                        password='Namin0707!!',
                        db='covid_19',
                        charset='utf8')

cursor = conn.cursor()

region_code = []
with open("K_COVID19.csv", 'r') as file:
    file_read = csv.reader(file)

  
    col = {
        'region_code' : 23,
        'province' : 4,
        'confirmed_date' : 10,
        'avg_temp' : 14,
        'min_temp' : 15,
        'max_temp' : 16}

    for i,line in enumerate(file_read):

        if not i:                           
            continue

        if ((line[col['region_code']],line[col['confirmed_date']]) in region_code) or (line[col['region_code']] == "NULL") or (line[col['confirmed_date']]=="NULL") :
            continue
        else:
            region_code.append((line[col['region_code']],line[col['confirmed_date']]))

        sql_data = []
        print(line)
        print(col.values())
        for j in col.values() :
            if line[j] == "NULL" :
                line[j] = None
            else:
                line[j] = line[j].strip()

            sql_data.append(line[j])
        print(sql_data)
        query = """INSERT INTO `WEATHER`(Region_code,Province,Wdate,Avg_temp,Min_temp,Max_temp) VALUES (%s,%s,%s,%s,%s,%s)"""
        sql_data = tuple(sql_data)
        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to WEATHER"%(line[col['region_code']]))
        except (pymysql.Error, pymysql.Warning) as e :
            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col['region_code']],e))
            break

conn.commit()
cursor.close()
