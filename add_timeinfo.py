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
        'test': 1,
        'negative': 2,
}
    con=0;
    rel=0;
    de=0;
    for i, line in enumerate(file_read):

        if not i:
            continue

        if (line[col_list['date']] in region_code) or (line[col_list['date']] == "NULL"):
            continue
        else:
            region_code.append(line[col_list['date']])
        sql_data = []
        print(line)
        print(col_list.values())
        for idx in col_list.values():
            if line[idx] == "NULL":
                line[idx] = None
            else:
                line[idx] = line[idx].strip()
            sql_data.append(line[idx])

        #받아온 date와 confirmed_date가 같은 patient의 수를 count
        confirmed="(SELECT COUNT(*) FROM PATIENTINFO WHERE confirmed_date = %s)"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(confirmed)
        result1=cursor.fetchall()
        con=con+int(result1[0][0])
        #누적으로 더하기
        
        #released_date 누적
        released = "(SELECT COUNT(*) FROM PATIENTINFO WHERE released_date = %s)"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(released)
        result2 = cursor.fetchall()
        rel = rel + int(result2[0][0])

        #deceased_date 누적
        deceased = "(SELECT COUNT(*) FROM PATIENTINFO WHERE deceased_date = %s)"%('"{}"'.format(line[col_list['date']]))
        cursor.execute(deceased)
        result3 = cursor.fetchall()
        de = de + int(result3[0][0])
        sql_data.append(con)
        sql_data.append(rel)
        sql_data.append(de)

        query = """INSERT INTO `TIMEINFO`(date,test,negative,confirmed,released,deceased) VALUES (%s,%s,%s,%s,%s,%s)"""
        print(sql_data[4])
        sql_data = tuple(sql_data)
        print(query)

        #누적한 값을 timeinfo에 넣기
        movie_vals = "%s,%s,%s,%s,%s,%s" % (
        '"{}"'.format(sql_data[0]), sql_data[1], sql_data[2],sql_data[3],sql_data[4],sql_data[5])
        sql = 'INSERT INTO TIMEINFO VALUES (%s)' % (movie_vals)
        try:
            cursor.execute(sql);
            print("inserting" )
        except pymysql.IntegrityError:
            print("%s is already in movie")
        sql="select confirmed from timeinfo"


    conn.commit()
cursor.close()
