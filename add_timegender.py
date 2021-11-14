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
    #누적을 저장할 변수
    con=0;
    rel=0;
    de=0;
    confe=0;
    defe=0;
    for i, line in enumerate(file_read):

        # Skip first line
        if not i:
            continue

        # checking duplicate region_code & checking region_code == "NULL"
        if (line[col_list['date']] in region_code) or (line[col_list['date']] == "NULL"):
            continue
        else:
            region_code.append(line[col_list['date']])
        # make sql data & query
        sql_data = []
        #print(line)
        # "NULL" -> None (String -> null)
        #print(col_list.values())
        for idx in col_list.values():
            if line[idx] == "NULL":
                line[idx] = None
            else:
                line[idx] = line[idx].strip()
            sql_data.append(line[idx])

        # 남자인경우
        sql2="male"

        # 받아온 date와 confirmed_date가 같고 남자인 patient의 수를 count
        confirmed="(SELECT COUNT(*) FROM PATIENTINFO WHERE confirmed_date = %s and sex=\"male\")"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(confirmed)
        result1=cursor.fetchall()
        con=con+int(result1[0][0])
        # 누적으로 더하기

        #deceased_date 누적
        deceased = "(SELECT COUNT(*) FROM PATIENTINFO WHERE deceased_date = %s and sex=\"male\")"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(deceased)
        result3 = cursor.fetchall()
        de = de + int(result3[0][0])
        sql_data.append(con)
        sql_data.append(de)
        #print(sql_data)

        query = """INSERT INTO `TIMEGENDER`(date,sex,confirmed,deceased) VALUES (%s,%s,%s,%s)"""
        #print(sql_data[4])
        sql_data = tuple(sql_data)
        #print(query)
        # print(sql_data)
        # for debug
        movie_vals = "%s,%s,%s,%s" % (
        '"{}"'.format(sql_data[0]), '"{}"'.format(sql2), con,de)
        print(sql_data[0])
        print(con)
        print(de)
        sql = 'INSERT INTO TIMEGENDER VALUES (%s)' % (movie_vals)
        try:
            cursor.execute(sql);
            print("inserting" )
        except pymysql.IntegrityError:
            print("%s is already in movie")
        sql="select confirmed from timeinfo"



        #여자인경우
        sql3="female"
        confirmed="(SELECT COUNT(*) FROM PATIENTINFO WHERE confirmed_date = %s and sex=\"female\")"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(confirmed)
        result4=cursor.fetchall()
        confe=confe+int(result4[0][0])

        deceased = "(SELECT COUNT(*) FROM PATIENTINFO WHERE deceased_date = %s and sex=\"female\")"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(deceased)
        result5 = cursor.fetchall()
        defe = defe + int(result5[0][0])
        #sql_data.append(confe)
        #sql_data.append(defe)
        #print(sql_data)

        #query = """INSERT INTO `TIMEGENDER`(date,sex,confirmed,deceased) VALUES (%s,%s,%s,%s)"""
        #print(sql_data[4])
        #sql_data = tuple(sql_data)
        #print(query)
        # print(sql_data)
        # for debug
        movie_vals = "%s,%s,%s,%s" % (
        '"{}"'.format(sql_data[0]), '"{}"'.format(sql3), confe,defe)
        print(sql_data[0])
        #print(con)
        #print(de)
        sql = 'INSERT INTO TIMEGENDER VALUES (%s)' % (movie_vals)
        try:
            cursor.execute(sql);
            print("inserting" )
        except pymysql.IntegrityError:
            print("%s is already in movie")
        sql="select confirmed from timeinfo"


    conn.commit()
cursor.close()
