## database_teamproject_3_db구축

###csv에서 읽고 저장

```python
with open("K_COVID19.csv", 'r') as file:
    file_read = csv.reader(file)

    col = {
        ...#들어갈 data의 이름과 해당 열을 매칭}

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
        query = """INSERT INTO table(column) VALUES (%s,%s)"""#insert value
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

```

###누적 데이터 삽입
```python
cursor = conn.cursor()

region_code = []
with open("addtional_Timeinfo.csv", 'r') as file:
    file_read = csv.reader(file)

    col_list = {
        'date': 0,
}#date는 additional_timeinfo에서 가져온다
    #각 index마다 누적을 저장할 배열
    con=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    rel=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    de=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
    
...

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
            de[j] = de[j] + int(result3[0][0])#누적값에 더한다
            
            value = "%s,%s,%s,%s,%s" % (
            '"{}"'.format(sql_data[0]), '"{}"'.format(age[j][0]), con[j],rel[j],de[j])

```
