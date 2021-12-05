## database teamproject #4차시
### 1.hospital table 넣기
#### database에 HOSPITAL 테이블을 생성 후 PATIENTINFO에 hospital_id column을 추가한다.
### 2.REGION table data 수정
#### 1)기존의 REGION table의 data는 대표 위도,경도 data가 없다(ex province=Seoul,city=Seoul)따라서 기존의 table을 
```Truncate table Region```
#### 으로 table의 데이터를 삭제한 후 Region.csv의 data를 읽어서 새로운 region data를 넣는다.
#### 2)PATIENTINFO의 data를 보면 city가 null이거나 etc인 경우가 있다.이러한 경우에는 PATIENTINFO와 REGION의 province와 city를 같도록 update한다.
```UPDATE PATIENTINFO SET city=province WHERE city IS NULL OR city="etc"```
### 3.hospital_id 넣기
#### hospital_id를 PATIENTINFO의 province와 city를 이용해서 region에서 latitude와 longitude의 값을 구하고, 해당 값을 HOSPITAL latitude와 longitude의 값과의 euclidean distance를 계산해서 가장 가까운 병원의 id를 PATIENTINFO에 넣고, HOSPITAL 테이블의 current의 값을 +1 한다.
### 4. hospital data를 출력하는 php
#### hospital_id를 입력받고 입력받은 값을 이용해서 PATIENTINFO에서 hospital_id가 같은 data를 select 해서 띄운다.
### 5. 출력한 hospital_id 를 클릭하면 해당 위치에 핀이 있는 google 지도 페이지로 이동
#### hospital.php에서 map.php로 herf속성을 통해 연결하고, hospital_id를 넘기면 map에서 HOSPITAL에서 해당 hospital_id를 가진 데이터를 SELECT 하고 latitude와 longitude를 이용해서 해당 위치에 핀을 찍는다, 그리고 name을 받아와서 핀에 출력한다.

## SQL task
### hospital.php에서 가장 많이 select 하는 PATIENTINFO의 hospital_id를 index로 생성
#### 1)index 생성 전
![image](https://user-images.githubusercontent.com/54846317/144766016-a67bcefd-ed40-4c12-aab4-518a8cc2c1dc.png)
#### 2) index 생성
![image](https://user-images.githubusercontent.com/54846317/144766061-f294d5cd-7a45-4bcf-9f38-8244e9a9b3de.png)
#### 3) index 생성 후
![image](https://user-images.githubusercontent.com/54846317/144766082-291dfb8a-1fbd-4f38-8d33-f274e416ada6.png)
#### 결과 : filtered 가 10.00에서 100.00으로 증가하였고 row수가 감소하였다.
