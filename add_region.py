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
        'region_code' :23,
        'province' :4,
        'city' : 5,
        'latitude' : 24,
        'longtitude' : 25,
        'elementary_school_count' :26,
        'kindergarten_count' : 27,
        'university_count' : 28,
        'academy_ratio' : 29,
        'elderly_population_ratio' : 30,
        'elderly_alone_ratio' : 31,
        'nursing_home_count' : 32}

    for i,line in enumerate(file_read):


        if not i:                           
            continue


        if (line[col['region_code']] in region_code) or (line[col['region_code']] == "NULL") :
            continue
        else:
            region_code.append(line[col['region_code']])

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
        query = """INSERT INTO `region`(region_code, province, city, latitude, longitude,
        elementary_school_count, kindergarten_count, university_count, academy_ratio, 
        elderly_population_ratio, eldery_alone_ratio, nursing_home_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql_data = tuple(sql_data)

        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to region"%(line[col['region_code']]))
        except (pymysql.Error, pymysql.Warning) as e :

            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col['region_code']],e))
            break

conn.commit()
cursor.close()
