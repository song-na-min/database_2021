# -*- coding: utf-8 -*-
import pymysql
import csv


conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='Namin0707!!',
                       db='covid_19',
                       charset='utf8')

cursor = conn.cursor()

region_code = []
with open("addtional_Timeinfo.csv", 'r') as file:
    file_read = csv.reader(file)

    col_list = {
        'date': 0,
}
    #각 province마다 누적을 저장할 배열
    con=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    rel=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    de=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    confe=0;
    defe=0;
    for i, line in enumerate(file_read):

        if not i:
            continue

        if (line[col_list['date']] in region_code) or (line[col_list['date']] == "NULL"):
            continue
        else:
            region_code.append(line[col_list['date']])

        sql_data = []


        for idx in col_list.values():
            if line[idx] == "NULL":
                line[idx] = None
            else:
                line[idx] = line[idx].strip()
            sql_data.append(line[idx])
        age="(SELECT DISTINCT PROVINCE FROM PATIENTINFO)"
        cursor.execute(age)
        age=cursor.fetchall()
        #province의 종류는 17가지
        #각 province마다 반복하면서
        for j in range(0,16):
            #해당 province이고 confirmed_date가 같은 patinet의 count
            confirmed="(SELECT COUNT(*) FROM PATIENTINFO WHERE confirmed_date = %s and province=%s)"%('"{}"'.format(line[col_list['date']]),'"{}"'.format(age[j][0]))
            cursor.execute(confirmed)
            result1=cursor.fetchall()
            con[j]=con[j]+int(result1[0][0])
            #해당 province list에 더해서 province의 종류에 따라 다른 누적값을 받도록

            #released
            released = "(SELECT COUNT(*) FROM PATIENTINFO WHERE released_date = %s and province=%s)" % (
            '"{}"'.format(line[col_list['date']]), '"{}"'.format(age[j][0]))
            cursor.execute(released)
            result4 = cursor.fetchall()
            rel[j] = rel[j] + int(result4[0][0])

            #deceased
            deceased = "(SELECT COUNT(*) FROM PATIENTINFO WHERE deceased_date = %s and province=%s)"%('"{}"'.format(line[col_list['date']]),'"{}"'.format(age[j][0]))
            cursor.execute(deceased)
            result3 = cursor.fetchall()
            de[j] = de[j] + int(result3[0][0])
            #sql_data.append(con)
            #sql_data.append(de)
            #print(sql_data)

            #query = """INSERT INTO `TIMEAGE`(date,age,confirmed,deceased) VALUES (%s,%s,%s,%s)"""
            #print(sql_data[4])
            #sql_data = tuple(sql_data)
            #print(query)
            # print(sql_data)
            # for debug
            movie_vals = "%s,%s,%s,%s,%s" % (
            '"{}"'.format(sql_data[0]), '"{}"'.format(age[j][0]), con[j],rel[j],de[j])
            #print(sql_data[0])
            #print(con)
            #print(de)
            sql = 'INSERT INTO TIMEPROVINCE VALUES (%s)' % (movie_vals)
            try:
                cursor.execute(sql);
                print("inserting" )
            except pymysql.IntegrityError:
                print("%s is already in movie")
            sql="select confirmed from timeinfo"

    conn.commit()
cursor.close()