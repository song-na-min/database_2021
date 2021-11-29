## database teamproject #3차시
### MySQL,APPACHE/PHP연동,search function,SQL tasks

### 3-2 테이블 하나에서 선택한 attribute를 기준으로 filtering한 data를 웹페이지에 출력
#### (1)state_patient_2.php
##### patientinfo 테이블에서 state를 선택해서 state별 환자 정보를 출력 
#### (2)province_case_2.php
##### case테이블에서 province를 선택하도록 해서 지역별 감염 case를 출력
#### (3)age_timeage_2.php
##### timeage테이블에서 age를 선택해서 나이별 누적감염 출력

### 3-3 5개의 테이블을 자유롭게 사용해서 하나의 의미있는 view를 생성한 후 웹페이지에 출력
#### view 생성
##### patientinfo 와 region 두 테이블을 province와 city가 같은 데이터 중 province,city,patient_id,age,infection_case,elementary_school_count를 select하여 view를 생성
```
CREATE VIEW patient_region AS 
SELECT P.Province,P.city,P.patient_id,P.age,P.infection_case,R.elementary_school_count
FROM PATIENTINFO AS P, REGION AS R 
WHERE P.province=R.province and R.city=P.city;
```
##### 생성한 view를 age를 기준으로 filtering하여 웹페이지에 출력하고, group by 를 이용해서 province, city별로 모아서 출력하고, order by province,city로 정렬해서 출력
