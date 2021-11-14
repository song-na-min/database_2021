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

case_id = []
with open("K_COVID19.csv", 'r') as file:
    file_read = csv.reader(file)

    col = {
        'case_id' : 17,
        'province' : 4,
        'city' : 5,
        'infection_group' : 19,
        'infection_case' : 6,
        'confirmed' : 20,
        'latitude' : 24,
        'longitude' : 25 }

    for i,line in enumerate(file_read):


        if not i:                           
            continue

        

        if (line[col['case_id']] in case_id) or (line[col['case_id']]=="NULL") :
            continue
        else:
            case_id.append(line[col['case_id']])


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
        query = """INSERT INTO CASEINFO(case_id,province,city,infection_group,
        infection_case,confirmed,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        sql_data = tuple(sql_data)

        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to CASEINFO"%(line[col['case_id']]))
        except (pymysql.Error, pymysql.Warning) as e :

            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col['case_id']],e))
            break

conn.commit()
cursor.close()

