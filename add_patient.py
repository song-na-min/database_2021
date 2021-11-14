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


patient_id = []
with open("K_COVID19.csv", 'r') as file:
    file_read = csv.reader(file)


    col = {
        'patient_id' :0,
        'sex' :1,
        'age' : 2,
        'country' : 3,
        'province' : 4,
        'city' :5,
        'infection_case' : 6,
        'infected_by' : 7,
        'contact_number' : 8,
        'symptom_onset_date' : 9,
        'confirmed_date' : 10,
        'released_date' : 11,
        'deceased_date' : 12,
        'state' : 13}

    for i,line in enumerate(file_read):


        if not i:                           
            continue


        if (line[col['patient_id']] in patient_id) or (line[col['patient_id']] == "NULL") :
            continue
        else:
            patient_id.append(line[col['patient_id']])


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
        query = """INSERT INTO `patientInfo`(patient_id,sex,age,country,province,city,infection_case,infect_by,contact_number,symptom_onset_date,confirmed_date,released_date,deceased_date,state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql_data = tuple(sql_data)

        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to patientInfo"%(line[col['patient_id']]))
        except (pymysql.Error, pymysql.Warning) as e :

            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col['patient_id']],e))
            break

conn.commit()
cursor.close()

print(len(patient_id))